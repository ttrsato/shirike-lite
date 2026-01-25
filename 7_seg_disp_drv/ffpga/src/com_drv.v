// Custom Module

module com_drv
  (
   input  wire       clk,
   input  wire       update_en,
   input  wire       rst_n,
   input  wire       com_cnt_en,
   output wire [2:0] mem_addr,
   output wire       com_ser,
   output wire       v_sync
   );

  reg [2:0] cnt;
  reg       vsync;
  
  assign com_ser = (cnt != 3'd1);
  assign mem_addr = cnt;
  assign v_sync = vsync;
  
  always @(posedge clk, negedge rst_n) begin
    if (!rst_n)
      cnt <= 'd0;
    else if ((cnt == 5) && com_cnt_en && update_en)
      cnt <= 'd0;
    else if (com_cnt_en && update_en)
      cnt <= cnt + 1'b1;
  end

  always @(posedge clk, negedge rst_n) begin
    if (!rst_n)
      vsync <= 1'b1;
    else if (cnt == 3'd5)
      vsync <= 1'b0;
    else
      vsync <= 1'b1;
  end

endmodule
