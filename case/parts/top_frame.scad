// ============================================================
// DaPao Space Mouse — Part 4: Top Frame (v3)
// Aligned to upper PCB (∅54mm):
//   - L/R switch posts at X=±10mm, Y=+12mm (matches SW4/SW5)
//   - PCB M2 mount posts at X=±15mm, Y=0 (matches H1/H2)
//   - Side switch cutouts at X=±frame_id/2, Y=0 (matches SW6/SW7)
// Print: upside down (flat ring face on bed), no supports.
// Qty: 1
// ============================================================
include <params.scad>

module top_frame() {
    frame_od = body_od_top;          // 60mm
    frame_id = frame_od - 2 * top_frame_wall;  // 54mm — PCB diameter fits exactly
    inner_r  = frame_id / 2;        // 27mm

    difference() {
        union() {
            // --- Outer ring wall ---
            difference() {
                cylinder(d = frame_od, h = top_frame_height);
                translate([0, 0, -0.1])
                    cylinder(d = frame_id, h = top_frame_height + 0.2);
            }

            // --- Solid floor (1.5mm) — ties everything together ---
            cylinder(d = frame_id - 0.2, h = 1.5);

            // --- Center divider (L/R button split) ---
            intersection() {
                translate([-top_frame_divider / 2, -inner_r, 0])
                    cube([top_frame_divider, frame_od, top_frame_height]);
                cylinder(d = frame_od, h = top_frame_height);
            }

            // --- Insertion lip into body shell top socket ---
            translate([0, 0, -top_frame_lip])
                difference() {
                    cylinder(d = body_od_top - 2 * body_wall - tol, h = top_frame_lip);
                    translate([0, 0, -0.1])
                        cylinder(d = frame_id - 2 * top_frame_wall, h = top_frame_lip + 0.2);
                }

            // --- L/R click switch posts (SW4 left, SW5 right) ---
            // Positions match PCB: X=±10mm, Y=+12mm
            for (x_side = [-1, 1]) {
                translate([x_side * top_sw_x, top_sw_offset_y, -top_sw_post_h])
                    cylinder(d = top_sw_post_d, h = top_sw_post_h);
                // Gusset connecting post base to floor
                translate([x_side * top_sw_x - top_sw_post_d / 2,
                           top_sw_offset_y - top_sw_post_d / 2,
                           -top_sw_post_h])
                    cube([top_sw_post_d,
                          top_sw_post_d / 2 + inner_r - top_sw_offset_y,
                          top_sw_post_h]);
            }

            // --- PCB M2 mount posts (H1 left, H2 right) ---
            // Positions match PCB: X=±15mm, Y=0
            for (x_side = [-1, 1]) {
                translate([x_side * top_mount_x, top_mount_y, -top_sw_post_h])
                    cylinder(d = top_sw_post_d, h = top_sw_post_h);
            }

            // --- Hinge shelves at back (Y-) for rocker buttons ---
            for (x_side = [-1, 1]) {
                translate([x_side * frame_id / 4 - top_btn_hinge_w / 2,
                           -inner_r, 0])
                    cube([top_btn_hinge_w, top_frame_wall + 2, top_frame_height]);
            }
        }

        // --- Trim everything outside the outer ring ---
        difference() {
            cylinder(d = frame_od + 20, h = top_frame_height + 2, center = true);
            cylinder(d = frame_od, h = top_frame_height + 3, center = true);
        }

        // --- L/R switch screw holes (M1.8) ---
        for (x_side = [-1, 1]) {
            translate([x_side * top_sw_x, top_sw_offset_y, -top_sw_post_h - 0.1])
                cylinder(d = pcb_screw_d, h = top_sw_post_h + 0.2);
        }

        // --- PCB mount screw holes (M2) ---
        for (x_side = [-1, 1]) {
            translate([x_side * top_mount_x, top_mount_y, -top_sw_post_h - 0.1])
                cylinder(d = 2.2, h = top_sw_post_h + 0.2);
        }

        // --- Side switch cutouts (SW6 Back / SW7 Fwd) ---
        // At X=±inner_r, Y=0 — switches face outward through frame wall
        for (x_side = [-1, 1]) {
            translate([x_side * (frame_od / 2 - top_frame_wall / 2),
                       -top_side_sw_w / 2,
                       (top_frame_height - top_side_sw_h) / 2])
                cube([top_frame_wall + 2, top_side_sw_w, top_side_sw_h]);
        }

        // --- Button clearance slots in floor (buttons press down) ---
        // Right half
        translate([top_frame_divider / 2 + top_btn_clearance, -inner_r + 0.1, -0.1])
            cube([inner_r - top_frame_divider / 2 - top_btn_clearance - 0.1,
                  frame_id - 0.2, 1.6]);
        // Left half
        translate([-inner_r + 0.1, -inner_r + 0.1, -0.1])
            cube([inner_r - top_frame_divider / 2 - top_btn_clearance - 0.1,
                  frame_id - 0.2, 1.6]);
    }
}

top_frame();
