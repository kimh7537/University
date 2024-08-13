module controller(
  input logic [5:0] iOp,
  output logic oRegWrite,
  output logic oMemWrite,
  output logic [2:0] oALUControl
);
  logic [8:0] signals;
  logic regdst, alusrc, branch, memtoreg, jump;
  logic [1:0] aluop;
  logic [5:0] funct;
  
  always_comb
    case(iOp)
      6'b100011: signals <= 9'b101001000;
      default: signals <= 9'b000000000;
    endcase
     
  assign {oRegWrite, regdst, alusrc, branch, oMemWrite, memtoreg, jump, aluop} = signals;
  
  always_comb
    case(aluop)
      2'b00: oALUControl = 3'b010;
      2'b01: oALUControl = 3'b110;
      default: case(funct)
        6'b100000: oALUControl = 3'b010;
        6'b100010: oALUControl = 3'b110;
        6'b100100: oALUControl = 3'b000;
        6'b100101: oALUControl = 3'b001;
        6'b101010: oALUControl = 3'b111;
      endcase
    endcase

endmodule
 
  
 