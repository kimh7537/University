// Code your design here
module alu(input logic [31:0] iA, iB, input logic [2:0] iF, 
           output logic [31:0] oY, output logic oZero);
  logic [31:0] temp;
  
  always_comb
      begin
      if(iF == 3'b000)
        oY = iA & iB;
      else if(iF == 3'b001)
        oY = iA | iB;
      else if(iF == 3'b010)
        oY = iA + iB;
      else if(iF == 3'b100)
        oY = iA & ~iB;
      else if(iF == 3'b101)
        oY = iA | ~iB;
      else if(iF == 3'b110)
        oY = iA - iB;
      else if(iF == 3'b111)
      begin
        temp = iA - iB;
        oY[31:1] = 31'h0;
        if(temp[31] == 1'b1)
          oY[0] = temp[31];
      end
      if(oY == 32'h00000000)
        oZero = 1;
      else
        oZero = 0;
    end
endmodule 

