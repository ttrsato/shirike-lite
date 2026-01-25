// Custom Module

module clk_div
  #(
    parameter CNT_MAX = 1000
    )
  (
   input  wire clk,
   input  wire rst_n,
   output wire strobe,
   output wire clk_int
   );
  
  reg  [13:0] div_cnt;
  reg         clk_i;
  
  assign strobe  = (div_cnt == (CNT_MAX - 1));
  assign clk_int = clk_i;
  
  always @(posedge clk, negedge rst_n) begin
    if (!rst_n) begin
      div_cnt <= 'd0;
    end
    else if (strobe) begin
      div_cnt <= 'd0;
    end
    else begin
      div_cnt <= div_cnt + 1'd1;
    end
  end
  
  always @(posedge clk, negedge rst_n) begin
    if (!rst_n)
      clk_i <= 1'b0;
    else if (strobe)
      clk_i <= (~clk_i);
  end  
  
endmodule
