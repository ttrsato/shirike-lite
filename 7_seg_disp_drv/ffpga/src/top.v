`timescale 1ns / 1ps
(* top *) module top
  (
   (* iopad_external_pin, clkbuf_inhibit *) input clk,
   (* iopad_external_pin *) input        rst_n,
   (* iopad_external_pin *) output       clk_en,
   // SEG                               
   (* iopad_external_pin *) output       seg_ser,
   (* iopad_external_pin *) output       seg_srclk,
   (* iopad_external_pin *) output       seg_rclk,
   (* iopad_external_pin *) output       seg_oe,
   (* iopad_external_pin *) output       seg_ser_oe,
   (* iopad_external_pin *) output       seg_srclk_oe,
   (* iopad_external_pin *) output       seg_rclk_oe,
   (* iopad_external_pin *) output       seg_oe_oe,
   // COM                                
   (* iopad_external_pin *) output       com_ser,
   (* iopad_external_pin *) output       com_srclk,
   (* iopad_external_pin *) output       com_rclk,
   (* iopad_external_pin *) output       com_oe,
   (* iopad_external_pin *) output       com_ser_oe,
   (* iopad_external_pin *) output       com_srclk_oe,
   (* iopad_external_pin *) output       com_rclk_oe,
   (* iopad_external_pin *) output       com_oe_oe,
   (* iopad_external_pin *) output       v_sync,
   (* iopad_external_pin *) output       v_sync_oe,
   // SPI                                
   (* iopad_external_pin *) input        spi_ss_n,
   (* iopad_external_pin *) input        spi_sck,
   (* iopad_external_pin *) input        spi_mosi,
   (* iopad_external_pin *) output       spi_miso,
   (* iopad_external_pin *) output       spi_miso_en,
   // BRAM
   (* iopad_external_pin *) output [1:0] BRAM0_RATIO,
   (* iopad_external_pin *) output [7:0] BRAM0_WDATA,
   (* iopad_external_pin *) output       BRAM0_nWEN,
   (* iopad_external_pin *) output       BRAM0_nWRITE_CLK,
   (* iopad_external_pin *) output       BRAM0_nWCLKEN,
   (* iopad_external_pin *) output [8:0] BRAM0_WADDR,
   (* iopad_external_pin *) output       BRAM0_nREN,
   (* iopad_external_pin *) output       BRAM0_nREAD_CLK,
   (* iopad_external_pin *) output       BRAM0_nRCLKEN,
   (* iopad_external_pin *) output [8:0] BRAM0_RADDR,
   (* iopad_external_pin *) input  [7:0] BRAM0_RDATA
   );
  
  //----------------------------------------------------
  // VARIABLE
  //----------------------------------------------------
  
  // SYS
  wire        clk_int;
  wire        strobe;
  wire        update_en;
  
  // Anote-common / Cathode-common (default)
  wire        anode_com = 1'b0;
  
  // DISP MEM
  wire  [7:0] mem_data_r;
  wire  [2:0] mem_addr_r;
  wire  [7:0] mem_data_w;
  wire  [2:0] mem_addr_w;
  //reg   [7:0] mem [0:5];
  reg  [47:0] mem;
  
  // COM-SEG
  wire        seg_ser_i;
  wire        com_ser_i;
  wire        seg_ld;
  
  // SPI
  wire [15:0] rx_data_wire;
  wire        rx_valid_pulse, rx_valid_pulse_rise;
  reg         rx_valid_pulse_d;
  
  //----------------------------------------------------
  // SIG DEFS
  //----------------------------------------------------
  
  // SYS
  assign clk_en              = 1'b1;
  assign update_en           = (~clk_int) & strobe;
  
  // SEG
  assign seg_ser             =  seg_ser_i ^ anode_com;
  assign seg_oe              =  1'b0;
  assign seg_ser_oe          =  1'b1;
  assign seg_srclk_oe        =  1'b1;
  assign seg_rclk_oe         =  1'b1;
  assign seg_oe_oe           =  1'b1;
  
  // COM
  assign com_ser             =  com_ser_i ^ anode_com;
  assign com_srclk           = ~seg_rclk;
  assign com_rclk            =  seg_rclk;
  assign com_oe              =  1'b0;
  assign com_ser_oe          =  1'b1;
  assign com_srclk_oe        =  1'b1;
  assign com_rclk_oe         =  1'b1;
  assign com_oe_oe           =  1'b1;
  assign v_sync_oe           =  1'b1;
  
  // SPI
  assign rx_valid_pulse_rise = (~rx_valid_pulse_d) & rx_valid_pulse;
  assign mem_addr_w          = rx_data_wire[10:8];
  assign mem_data_w          = rx_data_wire[7:0];
  
  //----------------------------------------------------
  // BRAM
  //----------------------------------------------------
  assign BRAM0_RATIO         = 2'b00; // 512 x 8
  assign BRAM0_WDATA         = mem_data_w;
  assign BRAM0_nWEN          = ~rx_valid_pulse_rise;
  assign BRAM0_nWRITE_CLK    = clk;
  assign BRAM0_nWCLKEN       = ~rx_valid_pulse_rise;
  assign BRAM0_WADDR         = {6'b0, mem_addr_w};
  assign BRAM0_nREN          = ~seg_ld;
  assign BRAM0_nREAD_CLK     = clk;
  assign BRAM0_nRCLKEN       = ~seg_ld;
  assign BRAM0_RADDR         = {6'b0, mem_addr_r};
  assign mem_data_r          = BRAM0_RDATA;
  
  //----------------------------------------------------
  // CLOCK DIV
  //----------------------------------------------------
  
  clk_div
    #(.CNT_MAX(8681))
  u_clk_div
    (
     .clk     ( clk      ),
     .rst_n   ( rst_n    ),
     .strobe  ( strobe   ),
     .clk_int ( clk_int  )
     );

  //----------------------------------------------------
  // SEG
  //----------------------------------------------------
  
  seg_drv u_seg_drv
    (
     .clk       ( clk        ),
     .clk_int   ( clk_int    ),
     .update_en ( update_en  ),
     .rst_n     ( rst_n      ),
     .data      ( mem_data_r ),
     .seg_srclk ( seg_srclk  ),
     .seg_ser   ( seg_ser_i  ),
     .seg_ld    ( seg_ld     ),
     .seg_rclk  ( seg_rclk   )
     );

  //----------------------------------------------------
  // COM
  //----------------------------------------------------
  
  com_drv u_com_drv
    (
     .clk        ( clk        ),
     .update_en  ( update_en  ),
     .rst_n      ( rst_n      ),
     .com_cnt_en ( seg_ld     ),
     .mem_addr   ( mem_addr_r ),
     .com_ser    ( com_ser_i  ),
     .v_sync     ( v_sync     )
     );
  
  //----------------------------------------------------
  // SPI Target
  //----------------------------------------------------
  
  spi_target 
    #(
      .CPOL  ( 1'b0 ),   // Standard Mode 0 (Idle Low)
      .CPHA  ( 1'b0 ),   // Standard Mode 0 (Sample Rising)
      .WIDTH ( 16   ),
      .LSB   ( 1'b0 )    // MSB First (Standard)
      )
  u_spi_target
    (
     // System Common
     .i_clk           ( clk            ),
     .i_rst_n         ( rst_n          ),
     .i_enable        ( 1'b1           ), // Enable the module permanently

     // SPI Physical Interface
     .i_ss_n          ( spi_ss_n       ),
     .i_sck           ( spi_sck        ),
     .i_mosi          ( spi_mosi       ),
     .o_miso          ( spi_miso       ),
     .o_miso_oe       ( spi_miso_en    ),

     // RX Interface (Data FROM MCU)
     .o_rx_data       ( rx_data_wire   ),
     .o_rx_data_valid ( rx_valid_pulse ),

     // TX Interface (Data TO MCU)
     .i_tx_data       ( rx_data_wire   ), 
     .o_tx_data_hold  (                )  // Not needed for simple echo
     );
  
  // Rise edge detect
  always @(posedge clk, negedge rst_n) begin
    if (!rst_n)
      rx_valid_pulse_d <= 1'b0;
    else
      rx_valid_pulse_d <= rx_valid_pulse;
  end
  
endmodule
