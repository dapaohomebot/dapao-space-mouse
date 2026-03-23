// ============================================================
// DaPao Space Mouse — Part 6: Right Top Button (v3)
// Plunger position updated to match SW5 on upper PCB (X=+10, Y=+12).
// Print: dome-side down, no supports.
// Qty: 1
// ============================================================
include <params.scad>

module top_button_right() {
    frame_id  = body_od_top - 2 * top_frame_wall;
    inner_r   = frame_id / 2;
    btn_r     = inner_r - top_btn_clearance;
    shell_h   = top_btn_height + top_btn_dome;
    clip_x_min = top_frame_divider / 2 + top_btn_clearance / 2;

    union() {
        // Half-disc dome
        intersection() {
            scale([1, 1, shell_h / btn_r])
                sphere(r = btn_r);
            translate([clip_x_min, -btn_r, -shell_h])
                cube([btn_r * 2, btn_r * 2, shell_h * 2]);
            cylinder(r = btn_r, h = shell_h + 0.1);
        }

        // Hinge tab at back (Y-)
        translate([clip_x_min / 2 + top_btn_hinge_w / 4,
                   -(btn_r - top_btn_hinge_t / 2), 0])
            cube([top_btn_hinge_w, top_btn_hinge_t, shell_h / 2], center = true);

        // Plunger post — matches SW5 position on PCB: X=+10mm, Y=+12mm
        translate([top_sw_x, top_sw_offset_y, 0])
            cylinder(d = top_btn_plunger_d, h = top_btn_plunger_h);
    }
}

top_button_right();
