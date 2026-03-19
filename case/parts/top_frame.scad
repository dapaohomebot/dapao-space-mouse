// ============================================================
// DaPao Space Mouse — Part 4: Top Frame
// Contains: outer ring, center divider, hinge shelves,
//           switch mount posts, insertion lip
// Print: upside down (flat ring on bed), no supports
// Qty: 1
// ============================================================
include <params.scad>

module top_frame() {
    frame_od = body_od_top;
    frame_id = frame_od - 2 * top_frame_wall;
    btn_r = frame_id / 2 - top_btn_clearance;

    difference() {
        union() {
            // Outer ring
            difference() {
                cylinder(d=frame_od, h=top_frame_height);
                translate([0, 0, -0.1])
                    cylinder(d=frame_id, h=top_frame_height + 0.2);
            }

            // Center divider (runs front to back along Y axis)
            translate([-top_frame_divider/2, -frame_od/2, 0])
                cube([top_frame_divider, frame_od, top_frame_height]);

            // Insertion lip (goes into body shell)
            translate([0, 0, -top_frame_lip])
                difference() {
                    cylinder(d=body_od_top - 2*body_wall - tol, h=top_frame_lip);
                    translate([0, 0, -0.1])
                        cylinder(d=body_od_top - 2*body_wall - tol - 4, h=top_frame_lip + 0.2);
                }

            // Switch mount posts (underneath, at front of each button half)
            translate([-frame_id/4, top_sw_offset_y, -top_sw_post_h])
                cylinder(d=top_sw_post_d, h=top_sw_post_h);
            translate([frame_id/4, top_sw_offset_y, -top_sw_post_h])
                cylinder(d=top_sw_post_d, h=top_sw_post_h);

            // Hinge shelves at back (Y-) for button pivot points
            translate([-frame_id/4, -(frame_id/2 - 2), 0])
                cube([top_btn_hinge_w + 2, 4, top_frame_height], center=true);
            translate([frame_id/4, -(frame_id/2 - 2), 0])
                cube([top_btn_hinge_w + 2, 4, top_frame_height], center=true);
        }

        // Trim divider and hinge shelves to cylinder boundary
        difference() {
            cylinder(d=frame_od + 10, h=100, center=true);
            cylinder(d=frame_od, h=101, center=true);
        }

        // Switch screw holes in posts
        translate([-frame_id/4, top_sw_offset_y, -top_sw_post_h - 0.1])
            cylinder(d=pcb_screw_d, h=top_sw_post_h + 0.2);
        translate([frame_id/4, top_sw_offset_y, -top_sw_post_h - 0.1])
            cylinder(d=pcb_screw_d, h=top_sw_post_h + 0.2);
    }
}

top_frame();
