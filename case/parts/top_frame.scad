// ============================================================
// DaPao Space Mouse — Part 4: Top Frame (v2)
// Fix: hinge shelves are now solid rectangles fused to the ring
//      inner wall — no floating geometry.
// Fix: switch posts attached to frame floor via solid bridge.
// Print: upside down (flat ring face on bed), no supports.
// Qty: 1
// ============================================================
include <params.scad>

module top_frame() {
    frame_od  = body_od_top;
    frame_id  = frame_od - 2 * top_frame_wall;
    frame_r   = frame_od / 2;
    inner_r   = frame_id / 2;

    difference() {
        union() {
            // Outer ring wall
            difference() {
                cylinder(d = frame_od, h = top_frame_height);
                translate([0, 0, -0.1])
                    cylinder(d = frame_id, h = top_frame_height + 0.2);
            }

            // Solid floor inside the ring (frame base) — ties everything together
            cylinder(d = frame_id - 0.2, h = 1.5);

            // Center divider (Y-axis, front to back)
            intersection() {
                translate([-top_frame_divider / 2, -frame_r, 0])
                    cube([top_frame_divider, frame_od, top_frame_height]);
                cylinder(d = frame_od, h = top_frame_height);
            }

            // Insertion lip (presses into body shell top socket)
            translate([0, 0, -top_frame_lip])
                difference() {
                    cylinder(d = body_od_top - 2 * body_wall - tol, h = top_frame_lip);
                    translate([0, 0, -0.1])
                        cylinder(d = body_od_top - 2 * body_wall - tol - 2 * top_frame_wall, h = top_frame_lip + 0.2);
                }

            // Hinge shelves at back (Y-) — solid blocks anchored to floor + ring wall
            for (x_side = [-1, 1]) {
                translate([x_side * frame_id / 4 - top_btn_hinge_w / 2,
                           -(inner_r),
                           0])
                    cube([top_btn_hinge_w, top_frame_wall + 2, top_frame_height]);
            }

            // Switch mount posts at front — standing from the floor
            for (x_side = [-1, 1]) {
                translate([x_side * frame_id / 4, top_sw_offset_y, -top_sw_post_h])
                    cylinder(d = top_sw_post_d, h = top_sw_post_h);
                // Bridge from post base to floor so it can't break off
                translate([x_side * frame_id / 4 - top_sw_post_d / 2,
                           top_sw_offset_y - top_sw_post_d / 2,
                           -top_sw_post_h])
                    cube([top_sw_post_d, top_sw_post_d / 2 + inner_r - top_sw_offset_y, top_sw_post_h]);
            }
        }

        // Trim everything to frame_od cylinder (removes protrusions outside ring)
        difference() {
            cylinder(d = frame_od + 20, h = top_frame_height + 2, center = true);
            cylinder(d = frame_od, h = top_frame_height + 3, center = true);
        }

        // Switch screw holes in posts
        for (x_side = [-1, 1]) {
            translate([x_side * frame_id / 4, top_sw_offset_y, -top_sw_post_h - 0.1])
                cylinder(d = pcb_screw_d, h = top_sw_post_h + 0.2);
        }

        // Button clearance slots — remove floor material inside each button half
        // so buttons can sink slightly without hitting the floor
        // Right half slot
        translate([top_frame_divider / 2 + top_btn_clearance, -inner_r + 0.1, -0.1])
            cube([inner_r - top_frame_divider / 2 - top_btn_clearance - 0.1, frame_id - 0.2, 1.7]);
        // Left half slot
        translate([-inner_r + 0.1, -inner_r + 0.1, -0.1])
            cube([inner_r - top_frame_divider / 2 - top_btn_clearance - 0.1, frame_id - 0.2, 1.7]);
    }
}

top_frame();
