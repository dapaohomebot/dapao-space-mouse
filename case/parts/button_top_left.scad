// ============================================================
// DaPao Space Mouse — Part 5: Left Top Button (Half-Circle Rocker)
// Hinges at back (Y-), clicks at front (Y+)
// The living hinge tab (~1mm thick) is intentional — allows flex
// Print: dome-side down, no supports needed
// Qty: 1
// ============================================================
include <params.scad>

module top_button(side) {
    frame_id = body_od_top - 2 * top_frame_wall;
    btn_r = frame_id / 2 - top_btn_clearance;

    difference() {
        union() {
            // Half-circle button body
            intersection() {
                difference() {
                    // Domed top surface
                    translate([0, 0, 0])
                        scale([1, 1, (top_btn_height + top_btn_dome) / btn_r])
                            sphere(r=btn_r);
                    // Hollow underneath
                    translate([0, 0, -btn_r])
                        scale([1, 1, (top_btn_height + top_btn_dome) / btn_r])
                            sphere(r=btn_r - 1.5);
                    // Cut off bottom hemisphere
                    translate([0, 0, -btn_r])
                        cube([2*btn_r, 2*btn_r, 2*btn_r], center=true);
                }

                // Trim to left half (X <= 0)
                translate([-(btn_r + 1), -(btn_r + 1), -1])
                    cube([btn_r + 1 - top_frame_divider/2 - top_btn_clearance/2,
                          2*(btn_r + 1),
                          top_btn_height + top_btn_dome + 2]);

                // Trim to within frame circle
                cylinder(r=btn_r, h=top_btn_height + top_btn_dome + 2);
            }

            // Hinge tab at back (Y-)
            translate([side * frame_id/4, -(btn_r - top_btn_hinge_w/2), 0])
                cube([top_btn_hinge_w, top_btn_hinge_w, top_btn_hinge_t], center=false);
        }
    }

    // Switch plunger contact (underneath, at front)
    translate([side * frame_id/4, top_sw_offset_y, -top_btn_plunger_h])
        cylinder(d=top_btn_plunger_d, h=top_btn_plunger_h);
}

top_button(-1);  // Left button
