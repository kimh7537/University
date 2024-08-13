// Code your design here
`include "alu.sv"
`include "regfile.sv"
`include "imem.sv"
`include "dmem.sv"

module datapath(
  input logic iClk,
  input logic iReset,
  input logic iRegWrite,
  input logic iMemWrite,
  input logic [2:0] iALUControl
);
  
  logic [31:0] pc, pcNext;
  logic [31:0] oRdata;
  
  logic [4:0] iRaddr1, iWaddr;
  logic [15:0] sign;

  logic [31:0]srcA;
  logic [31:0]signimm;
  
  logic [31:0]oY;
  
  logic [31:0]readData;

  always_ff @(posedge iClk, posedge iReset)
    if(iReset)
      pc <= 32'b0;
    else
      pc <= pcNext;
  	 
  imem instruction_memory(
    .iAddr		(pc),
    .oRdata		(oRdata)
  );
  
  assign iRaddr1 = oRdata[25:21];
  assign iWaddr = oRdata[20:16];
  assign sign[15:0] = oRdata[15:0];
  
  regfile register_file(
    .iClk		(iClk),
    .iReset		(iReset),
    .iRaddr1	(iRaddr1),
    .iWaddr		(iWaddr),
    .iWe		(iRegWrite),
    .iWdata		(readData),
    .oRdata1	(srcA)
  );

  always_comb
    begin
      if(sign[15]==1'b0)
        assign signimm = {{16{sign[15]}}, sign[15:0]};
      else if (sign[15] == 1'b1)
        assign signimm = {{16{sign[15]}}, sign[15:0]};
      else
        assign signimm = {4'h0, sign[15:0]};
    end

  
  alu alufile(
    .iA		(srcA),
    .iB		(signimm),
    .iF		(iALUControl),
    .oY		(oY)
  );
  
  dmem data_memory(
    .iClk		(iClk),
    .iWe		(iMemWrite),
    .iAddr		(oY),
    .oRdata		(readData)
  );
  
  assign pcNext = pc + 32'b100;
  
endmodule