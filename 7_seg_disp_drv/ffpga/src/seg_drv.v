// Custom Module

module seg_drv
  (
   input  wire       clk,
   input  wire       clk_int,
   input  wire       update_en,
   input  wire       rst_n,
   input  wire [7:0] data,
   output wire       seg_srclk,
   output wire       seg_ser,
   output wire       seg_ld,
   output wire       seg_rclk
   );
  //----------------------------------------------------
  // SEGMENT
  //----------------------------------------------------
  reg [2:0] seg_cnt;
  reg [7:0] seg_data;
  reg       seg_ld_lat;
  
  assign seg_ld = (seg_cnt == 3'd7);
  
  assign seg_srclk = ~clk_int;
  assign seg_ser   = seg_data[7];
  
  always @(posedge clk, negedge rst_n) begin
    if (!rst_n)
      seg_cnt <= 'd0;
    else if (update_en)
      seg_cnt <= seg_cnt + 1'b1;
  end

  always @(posedge clk, negedge rst_n) begin
    if (!rst_n)
      seg_data <= 'd0;
    else if (seg_ld && update_en)
      seg_data <= data;
    else if (update_en)
      seg_data <= {seg_data[6:0], 1'b0}; // shift left
  end
  
  reg seg_ld_d;
  always @(posedge clk, negedge rst_n) begin
    if (!rst_n)
      seg_ld_d <= 1'b0;
    else if (update_en)
      seg_ld_d <= seg_ld;
  end
  
  assign seg_rclk = seg_ld_d;
  
endmodule
