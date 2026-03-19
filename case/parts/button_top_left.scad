// ============================================================
// DaPao Space Mouse — Part 5: Left Top Button (v2)
// Half-circle rocker. Hinges at back (Y-), clicks at front (Y+).
// Fix: hinge tab now extends from the button body — always connected.
// Fix: plunger nub connected via a solid post through button shell.
// Print: dome-side down, no supports.
// Qty: 1
// ============================================================
include <params.scad>

module top_button_left() {
    frame_id = body_od_top - 2 * top_frame_wall;
    inner_r  = frame_id / 2;
    btn_r    = inner_r - top_btn_clearance;
    shell_h  = top_btn_height + top_btn_dome;

    // Left half: X <= -divider/2 - clearance/2
    clip_x_max = -(top_frame_divider / 2 + top_btn_clearance / 2);

    union() {
        // --- Main button half-disc ---
        intersection() {
            // Domed disc (solid — no hollowing, so it's printable and strong)
            scale([1, 1, shell_h / btn_r])
                sphere(r = btn_r);

            // Crop to left half only
            translate([-btn_r * 2, -btn_r, -shell_h])
                cube([btn_r * 2 + clip_x_max, btn_r * 2, shell_h * 2]);

            // Crop to within frame radius
            cylinder(r = btn_r, h = shell_h + 0.1);
        }

        // --- Hinge tab (back, Y-): flat tongue, firmly attached to body ---
        // Placed so its inner face is at btn_r from center (touching the frame hinge shelf)
        translate([clip_x_max / 2 - top_btn_hinge_w / 4,
                   -(btn_r - top_btn_hinge_t / 2),
                   0])
            cube([top_btn_hinge_w, top_btn_hinge_t, shell_h / 2], center = true);

        // --- Plunger post (front, Y+): solid cylinder, attached to underside ---
        // Rises from z=0 down (negative Z) to contact the switch
        translate([-inner_r / 4, top_sw_offset_y, 0])
            cylinder(d = top_btn_plunger_d, h = top_btn_plunger_h);
    }
}

top_button_left();
