// Code your design here
module regfile(input logic iClk, 
                input logic iReset,
                input logic [4:0] iRaddr1, iRaddr2, iWaddr,
                input logic [31:0] iWdata,
                input logic iWe,
                output logic [31:0] oRdata1, oRdata2);
  
  logic [31:0] registers[31:0];
  
  always_ff @(posedge iClk)
      if(iWe) 
        registers[iWaddr] <= iWdata;
  
  always_comb
    begin
      if(iRaddr1)
        oRdata1 = registers[iRaddr1];
      else
        oRdata1 = 32'h0;
          	
      if(iRaddr2)
        oRdata2 = registers[iRaddr2];
      else
        oRdata2 = 32'h0;
    end

endmodule