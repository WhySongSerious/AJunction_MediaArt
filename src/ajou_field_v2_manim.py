from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
from PIL import Image

from manim import (
    Animation,
    AnimationGroup,
    Arc,
    Arrow,
    Circle,
    Create,
    DashedLine,
    Dot,
    Ellipse,
    FadeIn,
    FadeOut,
    Flash,
    GrowFromCenter,
    ImageMobject,
    LaggedStart,
    Line,
    MoveAlongPath,
    ORIGIN,
    PI,
    Polygon,
    Rectangle,
    ReplacementTransform,
    Rotate,
    RoundedRectangle,
    Scene,
    Square,
    Succession,
    Transform,
    Triangle,
    VGroup,
    VMobject,
    config,
    linear,
    smooth,
    there_and_back,
    DOWN,
    LEFT,
    RIGHT,
    UP,
)
from manim.utils.rate_functions import ease_in_out_sine, ease_out_cubic

# -----------------------------------------------------------------------------
# Exact media-wall aspect ratio: 5200 / 1664 = 3.125.
# Resolution is selected from the CLI. Preview: 1600x512 / 24 fps.
# Final: 5200x1664 / 30 fps.
# -----------------------------------------------------------------------------
config.frame_width = 31.25
config.frame_height = 10.0
config.background_color = "#010611"

FRAME_W = 31.25
FRAME_H = 10.0
HALF_W = FRAME_W / 2
HALF_H = FRAME_H / 2

BG = "#010611"
BG_2 = "#03142A"
BLUE = "#0B5FB3"
AJOU_BLUE = "#1068BD"
SKY = "#64C7FF"
CYAN = "#42DDD0"
GOLD = "#E5B44B"
PALE_GOLD = "#FFE0A0"
SILVER = "#AFC3D7"
WHITE = "#F6FAFF"
GREEN = "#75E1B3"
VIOLET = "#9C8CFF"
RED = "#FF6D7C"

ROOT = Path(__file__).resolve().parent
LOGO_PATH = ROOT / "ajou_logo_symbol.png"


def polyline(points: Sequence[np.ndarray], color=SKY, width=1.6, opacity=1.0) -> VMobject:
    curve = VMobject()
    curve.set_points_smoothly(points)
    curve.set_stroke(color=color, width=width, opacity=opacity)
    return curve


def corner_path(points: Sequence[np.ndarray], color=SKY, width=1.5, opacity=1.0) -> VMobject:
    curve = VMobject()
    curve.set_points_as_corners(points)
    curve.set_stroke(color=color, width=width, opacity=opacity)
    return curve


def make_rotor(center: np.ndarray, radius: float, spokes: int, color: str, teeth: int = 16) -> VGroup:
    outer = Circle(radius=radius, color=color, stroke_width=2.0, stroke_opacity=0.8).move_to(center)
    mid = Circle(radius=radius * 0.67, color=BLUE, stroke_width=1.0, stroke_opacity=0.45).move_to(center)
    hub = Circle(radius=radius * 0.2, color=GOLD, stroke_width=1.5, stroke_opacity=0.9).move_to(center)
    spoke_group = VGroup()
    for i in range(spokes):
        a = 2 * PI * i / spokes
        p1 = center + np.array([math.cos(a), math.sin(a), 0]) * radius * 0.24
        p2 = center + np.array([math.cos(a), math.sin(a), 0]) * radius * 0.92
        spoke_group.add(Line(p1, p2, color=color, stroke_width=1.0, stroke_opacity=0.65))
    tooth_group = VGroup()
    for i in range(teeth):
        a = 2 * PI * i / teeth
        p = center + np.array([math.cos(a), math.sin(a), 0]) * radius
        tooth_group.add(
            Rectangle(
                width=radius * 0.16,
                height=radius * 0.08,
                color=color,
                stroke_width=0,
                fill_color=color,
                fill_opacity=0.55,
            ).rotate(a).move_to(p)
        )
    return VGroup(outer, mid, hub, spoke_group, tooth_group)


def make_node_network(
    center: np.ndarray,
    radius: float,
    count: int,
    seed: int,
    node_color: str = SKY,
    edge_color: str = BLUE,
    connection_steps: tuple[int, ...] = (1, 3),
) -> tuple[VGroup, VGroup, list[np.ndarray]]:
    rng = np.random.default_rng(seed)
    angles = np.linspace(0, 2 * PI, count, endpoint=False) + rng.uniform(-0.24, 0.24, count)
    radii = radius * rng.uniform(0.3, 1.0, count)
    pts = [center + np.array([math.cos(a) * r, math.sin(a) * r, 0]) for a, r in zip(angles, radii)]
    nodes = VGroup(*[Dot(p, radius=0.045 + 0.012 * (i % 4), color=node_color) for i, p in enumerate(pts)])
    edges = VGroup()
    for i in range(count):
        for step in connection_steps:
            j = (i + step) % count
            if np.linalg.norm(pts[i] - pts[j]) < radius * 1.55:
                edges.add(Line(pts[i], pts[j], color=edge_color, stroke_width=0.75, stroke_opacity=0.28))
    return nodes, edges, pts


def make_wave(x0: float, x1: float, y: float, amp: float, cycles: float, color: str, width: float = 1.8, phase: float = 0.0) -> VMobject:
    xs = np.linspace(x0, x1, 120)
    pts = [
        np.array([x, y + amp * math.sin(phase + cycles * 2 * PI * (x - x0) / (x1 - x0)), 0])
        for x in xs
    ]
    return polyline(pts, color=color, width=width, opacity=0.85)


def make_person(pos: np.ndarray, scale: float = 1.0, color: str = SILVER) -> VGroup:
    head = Circle(radius=0.16 * scale, color=color, stroke_width=1.1, stroke_opacity=0.9).move_to(pos + UP * 0.34 * scale)
    body = Line(pos + UP * 0.16 * scale, pos + DOWN * 0.28 * scale, color=color, stroke_width=1.25, stroke_opacity=0.9)
    arms = Line(pos + LEFT * 0.23 * scale, pos + RIGHT * 0.23 * scale, color=color, stroke_width=1.0, stroke_opacity=0.8)
    legs = VGroup(
        Line(pos + DOWN * 0.28 * scale, pos + DOWN * 0.55 * scale + LEFT * 0.17 * scale, color=color, stroke_width=1.0),
        Line(pos + DOWN * 0.28 * scale, pos + DOWN * 0.55 * scale + RIGHT * 0.17 * scale, color=color, stroke_width=1.0),
    )
    return VGroup(head, body, arms, legs)


def make_hex(center: np.ndarray, radius: float, color: str, opacity: float = 0.65, fill_opacity: float = 0.0) -> Polygon:
    pts = [center + np.array([math.cos(PI / 3 * i) * radius, math.sin(PI / 3 * i) * radius, 0]) for i in range(6)]
    return Polygon(*pts, color=color, stroke_width=1.3, stroke_opacity=opacity, fill_color=color, fill_opacity=fill_opacity)


def make_molecule(center: np.ndarray, scale: float, colors: tuple[str, str] = (SKY, GOLD), variant: int = 0) -> VGroup:
    patterns = (
        [(-0.55, 0.1), (0.0, 0.55), (0.55, 0.05), (0.2, -0.55)],
        [(-0.6, -0.25), (-0.15, 0.5), (0.45, 0.35), (0.55, -0.45), (-0.1, -0.5)],
        [(-0.55, 0.35), (0.05, 0.6), (0.6, 0.15), (0.35, -0.55), (-0.35, -0.5)],
    )
    pts = [center + np.array([x, y, 0]) * scale for x, y in patterns[variant % len(patterns)]]
    links = VGroup()
    for i in range(len(pts)):
        links.add(Line(pts[i], pts[(i + 1) % len(pts)], color=BLUE, stroke_width=1.0, stroke_opacity=0.65))
    nodes = VGroup(*[Dot(p, radius=0.095 * scale, color=colors[i % 2]) for i, p in enumerate(pts)])
    return VGroup(links, nodes)


class AjouFieldV2(Scene):
    """Textless geometric motion art, under 2 minutes, designed for 5200x1664."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.add(self.make_background())

        self.chapter_engineering()
        self.chapter_ict()
        self.chapter_software()
        self.chapter_natural_science()
        self.chapter_advanced_bio()
        self.chapter_pharmacy()
        self.chapter_medicine()
        self.chapter_nursing()
        self.chapter_business()
        self.chapter_social_sciences()
        self.chapter_humanities()
        self.chapter_international()
        self.chapter_open_major()
        self.chapter_logo_assembly()

    # ------------------------------------------------------------------
    # Persistent background
    # ------------------------------------------------------------------
    def make_background(self) -> VGroup:
        base = Rectangle(width=FRAME_W, height=FRAME_H, stroke_width=0, fill_color=BG, fill_opacity=1)
        glow_left = Circle(radius=6.7, color=AJOU_BLUE, stroke_width=0, fill_color=AJOU_BLUE, fill_opacity=0.035).move_to(np.array([-12.5, 0.0, 0]))
        glow_mid = Circle(radius=7.5, color=BLUE, stroke_width=0, fill_color=BLUE, fill_opacity=0.028).move_to(np.array([0.0, -1.8, 0]))
        glow_right = Circle(radius=6.2, color=SKY, stroke_width=0, fill_color=SKY, fill_opacity=0.018).move_to(np.array([12.0, 1.5, 0]))

        grid = VGroup()
        for x in np.linspace(-15, 15, 31):
            grid.add(Line(np.array([x, -5, 0]), np.array([x, 5, 0]), color=BLUE, stroke_width=0.35, stroke_opacity=0.07))
        for y in np.linspace(-4.5, 4.5, 10):
            grid.add(Line(np.array([-15.6, y, 0]), np.array([15.6, y, 0]), color=BLUE, stroke_width=0.35, stroke_opacity=0.06))

        arcs = VGroup()
        for i in range(5):
            arc = Arc(radius=11.0 + i * 1.1, start_angle=-PI * 0.18, angle=PI * 0.95, color=SKY, stroke_width=0.55, stroke_opacity=0.045)
            arc.stretch(1.6, 0).move_to(np.array([0, -5.0, 0]))
            arcs.add(arc)

        rng = np.random.default_rng(21)
        dust = VGroup()
        for i in range(80):
            x = rng.uniform(-15.3, 15.3)
            y = rng.uniform(-4.7, 4.7)
            r = rng.uniform(0.006, 0.021)
            c = GOLD if i % 9 == 0 else SKY
            dust.add(Dot(np.array([x, y, 0]), radius=r, color=c, fill_opacity=rng.uniform(0.08, 0.30)))

        return VGroup(base, glow_left, glow_mid, glow_right, grid, arcs, dust)

    # ------------------------------------------------------------------
    # Transition overlays: broad, multi-lane geometry. No single wandering line.
    # ------------------------------------------------------------------
    def transition_out(self, group: VGroup, mode: int = 0, direction: int = 1, run_time: float = 0.72) -> None:
        overlay = VGroup()
        animations: list[Animation] = []

        if mode % 3 == 0:
            for i, y in enumerate(np.linspace(-3.8, 3.8, 7)):
                phase = 0.55 * i
                pts = [
                    np.array([-16 * direction, y, 0]),
                    np.array([-8 * direction, y + 0.7 * math.sin(phase), 0]),
                    np.array([0, y * 0.28 + 0.55 * math.cos(phase), 0]),
                    np.array([8 * direction, -0.35 * y + 0.5 * math.sin(phase + 1.1), 0]),
                    np.array([16 * direction, -0.6 * y, 0]),
                ]
                p = polyline(pts, color=GOLD if i in (2, 4) else SKY, width=1.0 + 0.35 * (i % 2), opacity=0.42)
                overlay.add(p)
                animations.append(Create(p, rate_func=linear))
        elif mode % 3 == 1:
            for i in range(7):
                r = 0.7 + i * 0.9
                ring = Circle(radius=r, color=GOLD if i % 3 == 1 else SKY, stroke_width=1.0, stroke_opacity=0.28).move_to(np.array([direction * 8.5, 0, 0]))
                overlay.add(ring)
                animations.append(GrowFromCenter(ring, rate_func=ease_out_cubic))
        else:
            rng = np.random.default_rng(200 + mode)
            for i in range(48):
                s = Square(side_length=rng.uniform(0.08, 0.24), stroke_width=0, fill_color=GOLD if i % 7 == 0 else SKY, fill_opacity=rng.uniform(0.3, 0.8))
                s.move_to(np.array([rng.uniform(-15, 15), rng.uniform(-4.2, 4.2), 0]))
                s.rotate(rng.uniform(0, PI))
                overlay.add(s)
            animations.append(LaggedStart(*[sq.animate.shift(np.array([direction * 2.2, rng.uniform(-0.7, 0.7), 0])).rotate(PI / 2) for sq in overlay], lag_ratio=0.006))

        self.add(overlay)
        self.play(
            group.animate.shift(LEFT * direction * 1.4).scale(0.98).set_opacity(0),
            AnimationGroup(*animations, lag_ratio=0.03),
            run_time=run_time,
            rate_func=ease_in_out_sine,
        )
        self.remove(group)
        self.play(FadeOut(overlay, shift=RIGHT * direction * 0.45), run_time=0.24)

    # ------------------------------------------------------------------
    # 1. Engineering — force, structure, materials, transport, fluid.
    # ------------------------------------------------------------------
    def chapter_engineering(self) -> None:
        rotor_a = make_rotor(np.array([-12.4, 1.0, 0]), 1.45, 10, SKY, 18)
        rotor_b = make_rotor(np.array([-9.5, -1.55, 0]), 0.9, 8, GOLD, 14)

        lattice = VGroup()
        for r in range(-3, 4):
            for c in range(-4, 5):
                x = -2.8 + c * 0.72
                y = r * 0.64
                diamond = Polygon(
                    np.array([x, y + 0.26, 0]),
                    np.array([x + 0.31, y, 0]),
                    np.array([x, y - 0.26, 0]),
                    np.array([x - 0.31, y, 0]),
                    color=SKY if (r + c) % 4 == 0 else BLUE,
                    stroke_width=0.9,
                    stroke_opacity=0.52,
                    fill_color=SKY,
                    fill_opacity=0.025 if (r + c) % 4 else 0.12,
                )
                lattice.add(diamond)

        truss = VGroup()
        xs = np.linspace(4.5, 14.7, 12)
        lower = [np.array([x, -1.7 + 0.08 * math.sin(x), 0]) for x in xs]
        upper = [np.array([x, 1.2 + 0.65 * math.sin((x - 4.5) / 10.2 * PI), 0]) for x in xs]
        for i in range(len(xs) - 1):
            truss.add(Line(lower[i], lower[i + 1], color=SILVER, stroke_width=1.25, stroke_opacity=0.78))
            truss.add(Line(upper[i], upper[i + 1], color=SKY, stroke_width=1.45, stroke_opacity=0.82))
            truss.add(Line(lower[i], upper[i], color=BLUE, stroke_width=0.95, stroke_opacity=0.65))
            truss.add(Line(lower[i], upper[i + 1], color=GOLD if i % 3 == 0 else BLUE, stroke_width=0.85, stroke_opacity=0.62))
        truss.add(Line(lower[-1], upper[-1], color=BLUE, stroke_width=0.95, stroke_opacity=0.65))

        loads = VGroup(*[
            Arrow(np.array([x, 3.1 + 0.25 * (i % 2), 0]), np.array([x, 1.65 + 0.42 * math.sin((x - 4.5) / 10.2 * PI), 0]), color=GOLD, stroke_width=1.2, max_tip_length_to_length_ratio=0.18)
            for i, x in enumerate(np.linspace(5.2, 14.1, 7))
        ])

        flow_paths = VGroup()
        flow_dots = VGroup()
        for i, y in enumerate((-3.15, -2.72, -2.3)):
            p = make_wave(-14.8, 14.8, y, 0.22 + 0.05 * i, 4.5 + i * 0.6, CYAN if i == 1 else BLUE, width=1.0 + 0.3 * (i == 1), phase=i)
            flow_paths.add(p)
            flow_dots.add(Dot(p.get_start(), radius=0.075, color=GOLD if i == 1 else SKY))

        group = VGroup(rotor_a, rotor_b, lattice, truss, loads, flow_paths, flow_dots)
        self.play(
            LaggedStart(Create(rotor_a), Create(rotor_b), LaggedStart(*[Create(x) for x in lattice], lag_ratio=0.01), Create(truss), FadeIn(loads), Create(flow_paths), lag_ratio=0.09),
            run_time=1.15,
        )
        self.play(
            Rotate(rotor_a, angle=2.5 * PI, rate_func=linear),
            Rotate(rotor_b, angle=-3.2 * PI, rate_func=linear),
            lattice.animate(rate_func=there_and_back).apply_matrix([[1.0, 0.28], [0.0, 0.82]]).shift(UP * 0.15),
            truss.animate(rate_func=there_and_back).shift(UP * 0.38).scale(1.02),
            LaggedStart(*[a.animate(rate_func=there_and_back).shift(DOWN * 0.4) for a in loads], lag_ratio=0.08),
            *[MoveAlongPath(d, p, rate_func=linear) for d, p in zip(flow_dots, flow_paths)],
            run_time=4.55,
        )
        self.transition_out(group, mode=0, direction=1)

    # ------------------------------------------------------------------
    # 2. Advanced ICT — circuits, semiconductor, mobility control.
    # ------------------------------------------------------------------
    def chapter_ict(self) -> None:
        circuit_paths = VGroup()
        pulses = VGroup()
        paths: list[VMobject] = []
        ys = (-2.5, -1.55, -0.6, 0.55, 1.6, 2.55)
        for i, y in enumerate(ys):
            pts = [
                np.array([-15.2, y, 0]),
                np.array([-11.8, y, 0]),
                np.array([-10.8, y + 0.55 * (-1) ** i, 0]),
                np.array([-6.2, y + 0.55 * (-1) ** i, 0]),
                np.array([-5.2, 0.52 * y, 0]),
                np.array([-2.65, 0.52 * y, 0]),
            ]
            path = corner_path(pts, color=GOLD if i in (1, 4) else SKY, width=1.25, opacity=0.74)
            circuit_paths.add(path)
            paths.append(path)
            pulses.add(Dot(path.get_start(), radius=0.07, color=PALE_GOLD if i in (1, 4) else CYAN))

        chip_body = RoundedRectangle(width=5.1, height=4.2, corner_radius=0.25, color=SKY, stroke_width=1.8, stroke_opacity=0.85, fill_color=BG_2, fill_opacity=0.55)
        chip_core = Square(side_length=1.55, color=GOLD, stroke_width=1.6, fill_color=GOLD, fill_opacity=0.07)
        chip_cells = VGroup()
        for r in range(-2, 3):
            for c in range(-3, 4):
                cell = Square(side_length=0.28, stroke_width=0.7, stroke_color=BLUE, fill_color=SKY if (r + c) % 5 == 0 else BLUE, fill_opacity=0.28 if (r + c) % 5 == 0 else 0.04)
                cell.move_to(np.array([c * 0.5, r * 0.47, 0]))
                chip_cells.add(cell)
        pins = VGroup()
        for s in (-1, 1):
            for y in np.linspace(-1.55, 1.55, 8):
                pins.add(Line(np.array([s * 2.55, y, 0]), np.array([s * 3.15, y, 0]), color=SILVER, stroke_width=1.0, stroke_opacity=0.75))
            for x in np.linspace(-2.0, 2.0, 9):
                pins.add(Line(np.array([x, s * 2.1, 0]), np.array([x, s * 2.65, 0]), color=SILVER, stroke_width=1.0, stroke_opacity=0.75))
        chip = VGroup(chip_body, chip_core, chip_cells, pins).move_to(np.array([0, 0, 0]))

        tracks = VGroup()
        vehicles = VGroup()
        track_list: list[VMobject] = []
        for j in range(4):
            p = Arc(radius=2.2 + j * 0.48, start_angle=PI * 0.83, angle=PI * 1.36, color=SKY if j % 2 == 0 else BLUE, stroke_width=1.2, stroke_opacity=0.6)
            p.stretch(1.6, 0).move_to(np.array([10.1, -0.35 + j * 0.2, 0]))
            tracks.add(p)
            track_list.append(p)
            car = RoundedRectangle(width=0.46, height=0.22, corner_radius=0.06, color=GOLD if j == 1 else CYAN, stroke_width=0, fill_color=GOLD if j == 1 else CYAN, fill_opacity=0.9).move_to(p.get_start())
            vehicles.add(car)

        sensor_rings = VGroup(*[Circle(radius=0.35 + i * 0.48, color=GOLD if i == 1 else SKY, stroke_width=1.0, stroke_opacity=0.22).move_to(np.array([10.4, 0, 0])) for i in range(5)])

        group = VGroup(circuit_paths, pulses, chip, tracks, vehicles, sensor_rings)
        self.play(
            LaggedStart(Create(circuit_paths), FadeIn(pulses), GrowFromCenter(chip), Create(tracks), FadeIn(vehicles), FadeIn(sensor_rings), lag_ratio=0.08),
            run_time=1.05,
        )
        self.play(
            *[MoveAlongPath(d, p, rate_func=linear) for d, p in zip(pulses, paths)],
            chip_core.animate(rate_func=there_and_back).scale(1.45).rotate(PI / 2),
            LaggedStart(*[c.animate(rate_func=there_and_back).rotate(PI / 2).scale(1.2) for c in chip_cells], lag_ratio=0.01),
            *[MoveAlongPath(v, p, rate_func=linear) for v, p in zip(vehicles, track_list)],
            sensor_rings.animate(rate_func=there_and_back).scale(1.35).set_stroke(opacity=0.08),
            run_time=4.45,
        )
        self.transition_out(group, mode=1, direction=-1)

    # ------------------------------------------------------------------
    # 3. Software convergence — modular code, security, media, AI network.
    # ------------------------------------------------------------------
    def chapter_software(self) -> None:
        blocks = VGroup()
        for r in range(7):
            for c in range(10):
                s = Square(side_length=0.34, stroke_width=0.65, stroke_color=BLUE, fill_color=SKY if (r * 3 + c) % 7 == 0 else BLUE, fill_opacity=0.65 if (r * 3 + c) % 7 == 0 else 0.06)
                s.move_to(np.array([-13.9 + c * 0.56, -1.72 + r * 0.56, 0]))
                blocks.add(s)

        shield = Polygon(
            np.array([-1.55, 2.15, 0]),
            np.array([1.55, 2.15, 0]),
            np.array([2.05, 0.55, 0]),
            np.array([0, -2.4, 0]),
            np.array([-2.05, 0.55, 0]),
            color=GOLD,
            stroke_width=1.6,
            stroke_opacity=0.82,
            fill_color=GOLD,
            fill_opacity=0.025,
        )
        shield_mesh = VGroup()
        for i in range(8):
            y = -1.55 + i * 0.45
            shield_mesh.add(Line(np.array([-1.0 + 0.12 * i, y, 0]), np.array([1.0 - 0.12 * i, y, 0]), color=SKY, stroke_width=0.75, stroke_opacity=0.45))
        lock_core = VGroup(Circle(radius=0.42, color=SKY, stroke_width=1.2), Rectangle(width=0.7, height=0.9, color=SKY, stroke_width=1.2, fill_color=SKY, fill_opacity=0.03).shift(DOWN * 0.45))
        shield_group = VGroup(shield, shield_mesh, lock_core)

        nodes, edges, _ = make_node_network(np.array([10.4, 0.0, 0]), 3.35, 28, 77, node_color=CYAN, edge_color=VIOLET, connection_steps=(1, 4, 7))
        neural = VGroup(edges, nodes)
        output_pixels = VGroup()
        rng = np.random.default_rng(45)
        for i in range(58):
            px = Square(side_length=rng.uniform(0.10, 0.28), stroke_width=0, fill_color=GOLD if i % 11 == 0 else SKY, fill_opacity=rng.uniform(0.18, 0.75))
            px.move_to(np.array([rng.uniform(6.4, 14.6), rng.uniform(-3.6, 3.6), 0]))
            output_pixels.add(px)

        scan = Rectangle(width=6.1, height=0.2, stroke_width=0, fill_color=CYAN, fill_opacity=0.34).move_to(np.array([-11.2, -2.3, 0]))
        group = VGroup(blocks, shield_group, neural, output_pixels, scan)
        self.play(
            LaggedStart(FadeIn(blocks, scale=0.7), GrowFromCenter(shield_group), FadeIn(neural, scale=0.8), FadeIn(output_pixels), FadeIn(scan), lag_ratio=0.08),
            run_time=1.0,
        )

        block_anims = []
        for i, b in enumerate(blocks):
            dx = 0.45 * math.cos(i * 0.7)
            dy = 0.5 * math.sin(i * 1.1)
            block_anims.append(b.animate(rate_func=there_and_back).shift(np.array([dx, dy, 0])).rotate(PI / 4).scale(1.08))
        pixel_anims = []
        for i, p in enumerate(output_pixels):
            pixel_anims.append(p.animate(rate_func=there_and_back).shift(np.array([0.5 * math.sin(i), 0.65 * math.cos(i * 0.8), 0])).rotate(PI / 2))

        self.play(
            LaggedStart(*block_anims, lag_ratio=0.008),
            scan.animate.shift(UP * 4.6),
            shield_group.animate(rate_func=there_and_back).scale(1.12),
            Rotate(lock_core, angle=2 * PI, rate_func=linear),
            Rotate(neural, angle=PI * 0.8, rate_func=there_and_back),
            nodes.animate(rate_func=there_and_back).scale(1.55),
            LaggedStart(*pixel_anims, lag_ratio=0.006),
            run_time=4.45,
        )
        self.transition_out(group, mode=2, direction=1)

    # ------------------------------------------------------------------
    # 4. Natural sciences — mathematics, waves, matter, life.
    # ------------------------------------------------------------------
    def chapter_natural_science(self) -> None:
        grid = VGroup()
        for x in np.linspace(-14.8, -6.0, 12):
            grid.add(Line(np.array([x, -3.4, 0]), np.array([x, 3.4, 0]), color=BLUE, stroke_width=0.55, stroke_opacity=0.22))
        for y in np.linspace(-3.0, 3.0, 9):
            grid.add(Line(np.array([-15.0, y, 0]), np.array([-5.8, y, 0]), color=BLUE, stroke_width=0.55, stroke_opacity=0.22))
        axis_x = Arrow(np.array([-14.9, 0, 0]), np.array([-5.9, 0, 0]), color=SILVER, stroke_width=1.0, max_tip_length_to_length_ratio=0.04)
        axis_y = Arrow(np.array([-10.4, -3.3, 0]), np.array([-10.4, 3.3, 0]), color=SILVER, stroke_width=1.0, max_tip_length_to_length_ratio=0.05)
        f1 = polyline([np.array([x, 1.2 * math.sin((x + 15) * 1.35) * math.exp(-0.045 * (x + 10.4) ** 2), 0]) for x in np.linspace(-14.9, -5.9, 130)], color=GOLD, width=2.0)
        f2 = polyline([np.array([x, 1.6 * math.sin((x + 15) * 2.1 + 1.1) * math.exp(-0.065 * (x + 10.4) ** 2), 0]) for x in np.linspace(-14.9, -5.9, 130)], color=CYAN, width=1.8)

        atom_center = np.array([0, 0, 0])
        nucleus = VGroup(Dot(atom_center + LEFT * 0.12, radius=0.16, color=GOLD), Dot(atom_center + RIGHT * 0.12, radius=0.16, color=SKY))
        orbits = VGroup()
        electrons = VGroup()
        for i, ang in enumerate((0, PI / 3, -PI / 3, PI / 2)):
            orbit = Ellipse(width=5.0, height=1.75, color=SKY if i != 2 else GOLD, stroke_width=1.05, stroke_opacity=0.55).rotate(ang)
            orbits.add(orbit)
            electrons.add(Dot(orbit.get_start(), radius=0.075, color=PALE_GOLD if i % 2 == 0 else CYAN))
        atom = VGroup(orbits, electrons, nucleus)

        cell_outline = Circle(radius=1.55, color=GREEN, stroke_width=1.5, stroke_opacity=0.72, fill_color=GREEN, fill_opacity=0.02).move_to(np.array([10.2, 0, 0]))
        cell_core = Circle(radius=0.48, color=GOLD, stroke_width=1.2, stroke_opacity=0.75).move_to(np.array([10.45, -0.1, 0]))
        organelles = VGroup(*[
            Ellipse(width=0.72, height=0.28, color=SKY, stroke_width=0.8, stroke_opacity=0.5).rotate(a).move_to(np.array([10.2 + 0.9 * math.cos(a), 0.75 * math.sin(a), 0]))
            for a in np.linspace(0, 2 * PI, 8, endpoint=False)
        ])
        daughter_a = VGroup(Circle(radius=1.05, color=GREEN, stroke_width=1.35), Circle(radius=0.32, color=GOLD, stroke_width=1.0)).move_to(np.array([8.8, 0, 0])).set_opacity(0)
        daughter_b = VGroup(Circle(radius=1.05, color=GREEN, stroke_width=1.35), Circle(radius=0.32, color=GOLD, stroke_width=1.0)).move_to(np.array([12.2, 0, 0])).set_opacity(0)

        group = VGroup(grid, axis_x, axis_y, f1, atom, cell_outline, cell_core, organelles, daughter_a, daughter_b)
        self.play(
            LaggedStart(Create(grid), Create(axis_x), Create(axis_y), Create(f1), GrowFromCenter(atom), GrowFromCenter(VGroup(cell_outline, cell_core, organelles)), lag_ratio=0.09),
            run_time=1.05,
        )
        self.play(
            Transform(f1, f2),
            *[MoveAlongPath(e, o, rate_func=linear) for e, o in zip(electrons, orbits)],
            Rotate(orbits, angle=PI * 0.65, rate_func=there_and_back),
            cell_outline.animate.scale(0.74).set_opacity(0),
            cell_core.animate.scale(0.65).set_opacity(0),
            organelles.animate.scale(0.7).set_opacity(0),
            daughter_a.animate.set_opacity(1).shift(LEFT * 0.5),
            daughter_b.animate.set_opacity(1).shift(RIGHT * 0.5),
            run_time=4.4,
        )
        self.transition_out(group, mode=0, direction=-1)

    # ------------------------------------------------------------------
    # 5. Advanced biotechnology — DNA, protein folding, biomaterial, digital bio.
    # ------------------------------------------------------------------
    def chapter_advanced_bio(self) -> None:
        xs = np.linspace(-14.7, -5.4, 30)
        dna = VGroup()
        dna_target = VGroup()
        for i, x in enumerate(xs):
            y1 = 1.55 * math.sin((x + 14.7) * 1.9)
            y2 = -y1
            y1b = 1.55 * math.sin((x + 14.7) * 1.9 + PI * 0.92)
            y2b = -y1b
            c = SKY if i % 2 == 0 else CYAN
            dna.add(Dot(np.array([x, y1, 0]), radius=0.05, color=c))
            dna.add(Dot(np.array([x, y2, 0]), radius=0.05, color=c))
            dna.add(Line(np.array([x, y1, 0]), np.array([x, y2, 0]), color=BLUE, stroke_width=0.72, stroke_opacity=0.44))
            dna_target.add(Dot(np.array([x, y1b, 0]), radius=0.05, color=c))
            dna_target.add(Dot(np.array([x, y2b, 0]), radius=0.05, color=c))
            dna_target.add(Line(np.array([x, y1b, 0]), np.array([x, y2b, 0]), color=BLUE, stroke_width=0.72, stroke_opacity=0.44))

        # Protein folding: a long chain folds into a compact geometric loop.
        chain_pts = [np.array([-4.2 + i * 0.42, 2.2 * math.sin(i * 0.48) * math.exp(-0.012 * (i - 12) ** 2), 0]) for i in range(25)]
        protein = polyline(chain_pts, color=GOLD, width=1.8, opacity=0.75)
        target_pts = []
        for i in range(25):
            a = i * 0.58
            r = 2.2 - 0.055 * i
            target_pts.append(np.array([0.4 + r * math.cos(a), r * 0.62 * math.sin(a), 0]))
        protein_target = polyline(target_pts, color=GOLD, width=1.8, opacity=0.84)
        beads = VGroup(*[Dot(p, radius=0.055, color=PALE_GOLD if i % 5 == 0 else SKY) for i, p in enumerate(chain_pts[::2])])

        weave = VGroup()
        for i in range(9):
            weave.add(make_wave(6.2, 14.7, -2.8 + i * 0.7, 0.23, 2.3 + 0.15 * i, SKY if i % 2 == 0 else BLUE, width=0.9, phase=i * 0.5))
        for i in range(10):
            x = 6.4 + i * 0.9
            weave.add(polyline([np.array([x, -3.2, 0]), np.array([x + 0.45 * math.sin(i), 0, 0]), np.array([x, 3.2, 0])], color=GOLD if i % 3 == 0 else CYAN, width=0.7, opacity=0.32))
        bio_nodes, bio_edges, _ = make_node_network(np.array([10.6, 0, 0]), 2.85, 24, 123, node_color=GREEN, edge_color=SKY, connection_steps=(1, 5))
        digital_bio = VGroup(bio_edges, bio_nodes)

        group = VGroup(dna, protein, beads, weave, digital_bio)
        self.play(
            LaggedStart(FadeIn(dna), Create(protein), FadeIn(beads), Create(weave), FadeIn(digital_bio), lag_ratio=0.08),
            run_time=1.0,
        )
        self.play(
            Transform(dna, dna_target),
            Transform(protein, protein_target),
            beads.animate(rate_func=there_and_back).scale(1.45),
            weave.animate(rate_func=there_and_back).apply_matrix([[1.0, 0.22], [0.0, 0.84]]),
            Rotate(digital_bio, angle=PI * 0.75, rate_func=there_and_back),
            bio_nodes.animate(rate_func=there_and_back).scale(1.45),
            run_time=4.35,
        )
        self.transition_out(group, mode=1, direction=1)

    # ------------------------------------------------------------------
    # 6. Pharmacy — capsule, controlled release, molecular docking, dosage.
    # ------------------------------------------------------------------
    def chapter_pharmacy(self) -> None:
        capsule_a = RoundedRectangle(width=3.3, height=1.25, corner_radius=0.62, color=SKY, stroke_width=1.65, fill_color=BLUE, fill_opacity=0.06).rotate(PI / 7).move_to(np.array([-12.2, 1.35, 0]))
        capsule_a.add(Line(capsule_a.get_center() + UP * 0.7, capsule_a.get_center() + DOWN * 0.7, color=GOLD, stroke_width=1.2).rotate(PI / 7, about_point=capsule_a.get_center()))
        capsule_b = RoundedRectangle(width=2.6, height=1.0, corner_radius=0.5, color=GOLD, stroke_width=1.4, fill_color=GOLD, fill_opacity=0.04).rotate(-PI / 8).move_to(np.array([-9.0, -1.4, 0]))
        capsule_b.add(Line(capsule_b.get_center() + UP * 0.55, capsule_b.get_center() + DOWN * 0.55, color=SKY, stroke_width=1.0).rotate(-PI / 8, about_point=capsule_b.get_center()))

        release_paths = VGroup()
        particles = VGroup()
        path_list: list[VMobject] = []
        for i in range(12):
            y0 = 1.2 + 0.15 * math.sin(i)
            pts = [
                np.array([-10.6, y0, 0]),
                np.array([-7.2, 0.9 * math.sin(i * 0.7), 0]),
                np.array([-4.2, 1.8 * math.sin(i * 0.4 + 0.6), 0]),
            ]
            p = polyline(pts, color=BLUE, width=0.65, opacity=0.24)
            release_paths.add(p)
            path_list.append(p)
            particles.add(Dot(p.get_start(), radius=0.045 + 0.01 * (i % 3), color=GOLD if i % 4 == 0 else SKY))

        receptor = make_hex(np.array([0, 0, 0]), 2.55, SKY, opacity=0.72, fill_opacity=0.02)
        receptor_inner = make_hex(np.array([0, 0, 0]), 1.2, GOLD, opacity=0.78, fill_opacity=0.025)
        docking_slots = VGroup(*[make_hex(np.array([2.55 * math.cos(PI / 3 * i), 2.55 * math.sin(PI / 3 * i), 0]), 0.38, BLUE, opacity=0.48) for i in range(6)])
        mol_good = make_molecule(np.array([-4.3, -0.4, 0]), 0.9, (GOLD, SKY), variant=1)
        mol_bad_a = make_molecule(np.array([-3.8, 2.6, 0]), 0.78, (CYAN, SKY), variant=0)
        mol_bad_b = make_molecule(np.array([-3.7, -2.8, 0]), 0.78, (VIOLET, SKY), variant=2)

        dose_rings = VGroup(*[Circle(radius=0.55 + i * 0.62, color=GOLD if i in (1, 4) else SKY, stroke_width=1.0, stroke_opacity=0.32 - i * 0.035).move_to(np.array([10.7, 0, 0])) for i in range(6)])
        dose_particles = VGroup()
        rng = np.random.default_rng(7)
        for i in range(38):
            a = rng.uniform(0, 2 * PI)
            r = rng.uniform(0.6, 3.3)
            dose_particles.add(Dot(np.array([10.7 + r * math.cos(a), r * math.sin(a), 0]), radius=rng.uniform(0.025, 0.06), color=GOLD if i % 6 == 0 else SKY))

        group = VGroup(capsule_a, capsule_b, release_paths, particles, receptor, receptor_inner, docking_slots, mol_good, mol_bad_a, mol_bad_b, dose_rings, dose_particles)
        self.play(
            LaggedStart(GrowFromCenter(capsule_a), GrowFromCenter(capsule_b), Create(release_paths), FadeIn(particles), GrowFromCenter(VGroup(receptor, receptor_inner, docking_slots)), FadeIn(VGroup(mol_good, mol_bad_a, mol_bad_b)), GrowFromCenter(dose_rings), FadeIn(dose_particles), lag_ratio=0.07),
            run_time=1.0,
        )
        self.play(
            capsule_a.animate(rate_func=there_and_back).rotate(-PI / 2).shift(RIGHT * 0.4),
            capsule_b.animate(rate_func=there_and_back).rotate(PI / 2).shift(LEFT * 0.3),
            *[MoveAlongPath(d, p, rate_func=linear) for d, p in zip(particles, path_list)],
            mol_good.animate.move_to(ORIGIN).scale(1.1),
            mol_bad_a.animate.shift(UP * 1.2 + LEFT * 0.8).set_opacity(0.2),
            mol_bad_b.animate.shift(DOWN * 1.2 + LEFT * 0.8).set_opacity(0.2),
            receptor_inner.animate(rate_func=there_and_back).rotate(PI).scale(1.25),
            dose_rings.animate(rate_func=there_and_back).scale(1.32).set_stroke(opacity=0.08),
            dose_particles.animate(rate_func=there_and_back).scale(0.28, about_point=np.array([10.7, 0, 0])),
            run_time=4.0,
        )
        self.transition_out(group, mode=2, direction=-1)

    # ------------------------------------------------------------------
    # 7. Medicine — diagnostic imaging, anatomy, detection, repair.
    # ------------------------------------------------------------------
    def chapter_medicine(self) -> None:
        # Geometric body / anatomy schematic.
        head = Circle(radius=0.72, color=SILVER, stroke_width=1.25, stroke_opacity=0.8).move_to(np.array([-10.8, 2.4, 0]))
        torso_outline = polyline([
            np.array([-10.8, 1.65, 0]),
            np.array([-12.25, 0.9, 0]),
            np.array([-12.0, -2.4, 0]),
            np.array([-9.6, -2.4, 0]),
            np.array([-9.35, 0.9, 0]),
            np.array([-10.8, 1.65, 0]),
        ], color=SILVER, width=1.35, opacity=0.82)
        spine = Line(np.array([-10.8, 1.45, 0]), np.array([-10.8, -2.1, 0]), color=GOLD, stroke_width=1.0, stroke_opacity=0.68)
        lungs = VGroup(
            Ellipse(width=1.1, height=1.9, color=SKY, stroke_width=1.0, stroke_opacity=0.55).move_to(np.array([-11.45, 0.25, 0])),
            Ellipse(width=1.1, height=1.9, color=SKY, stroke_width=1.0, stroke_opacity=0.55).move_to(np.array([-10.15, 0.25, 0])),
        )
        body = VGroup(head, torso_outline, spine, lungs)

        scanner = VGroup(
            RoundedRectangle(width=5.0, height=7.2, corner_radius=0.55, color=BLUE, stroke_width=1.0, stroke_opacity=0.35).move_to(np.array([-10.8, 0, 0])),
            Arc(radius=2.7, start_angle=-PI / 2, angle=PI, color=SKY, stroke_width=1.8, stroke_opacity=0.55).move_to(np.array([-10.8, 0, 0])),
            Arc(radius=2.7, start_angle=PI / 2, angle=PI, color=SKY, stroke_width=1.8, stroke_opacity=0.55).move_to(np.array([-10.8, 0, 0])),
        )
        scan_line = Rectangle(width=4.6, height=0.15, stroke_width=0, fill_color=CYAN, fill_opacity=0.55).move_to(np.array([-10.8, 3.0, 0]))

        slices = VGroup()
        anomaly = VGroup()
        for i, x in enumerate((-2.7, 0.0, 2.7)):
            ring = VGroup(
                Circle(radius=1.55, color=SKY, stroke_width=1.1, stroke_opacity=0.62),
                Circle(radius=1.05, color=BLUE, stroke_width=0.8, stroke_opacity=0.45),
                Circle(radius=0.5, color=SILVER, stroke_width=0.7, stroke_opacity=0.4),
            ).move_to(np.array([x, 0, 0]))
            slices.add(ring)
            anomaly.add(make_hex(np.array([x + 0.4 * (-1) ** i, 0.45 - 0.35 * i, 0]), 0.23, GOLD, opacity=0.9, fill_opacity=0.22))

        tissue = VGroup()
        tissue_targets = VGroup()
        missing_index = 18
        count = 0
        for r in range(-3, 4):
            for c in range(-4, 5):
                center = np.array([10.8 + c * 0.62, r * 0.58, 0])
                cell = make_hex(center, 0.30, GREEN if (r + c) % 3 == 0 else SKY, opacity=0.46, fill_opacity=0.035)
                if count == missing_index:
                    cell.set_opacity(0.0)
                tissue.add(cell)
                target = cell.copy().set_opacity(1.0)
                tissue_targets.add(target)
                count += 1
        repair_fragment = make_hex(np.array([6.7, -3.4, 0]), 0.30, GOLD, opacity=0.9, fill_opacity=0.2)
        repair_target = tissue_targets[missing_index].get_center()

        group = VGroup(body, scanner, scan_line, slices, anomaly, tissue, repair_fragment)
        self.play(
            LaggedStart(Create(body), Create(scanner), FadeIn(scan_line), GrowFromCenter(slices), FadeIn(anomaly), FadeIn(tissue), GrowFromCenter(repair_fragment), lag_ratio=0.08),
            run_time=1.0,
        )
        self.play(
            scan_line.animate.shift(DOWN * 6.0),
            Rotate(scanner[1], angle=PI * 1.4, rate_func=linear),
            Rotate(scanner[2], angle=-PI * 1.4, rate_func=linear),
            lungs.animate(rate_func=there_and_back).scale(1.12),
            LaggedStart(*[r.animate(rate_func=there_and_back).scale(1.22).rotate(PI / 4) for r in slices], lag_ratio=0.12),
            anomaly.animate(rate_func=there_and_back).scale(1.8),
            repair_fragment.animate.move_to(repair_target).rotate(2 * PI).scale(1.02),
            tissue[missing_index].animate.set_opacity(1.0),
            run_time=4.3,
        )
        self.transition_out(group, mode=0, direction=1)

    # ------------------------------------------------------------------
    # 8. Nursing — bedside care, continuous monitoring, stability, handover.
    # ------------------------------------------------------------------
    def chapter_nursing(self) -> None:
        # Bed and patient are intentionally direct, but drawn as clean geometry.
        bed_frame = VGroup(
            RoundedRectangle(width=7.0, height=1.45, corner_radius=0.25, color=SKY, stroke_width=1.4, stroke_opacity=0.75, fill_color=BLUE, fill_opacity=0.035).move_to(np.array([-9.8, -1.25, 0])),
            Line(np.array([-13.3, -2.0, 0]), np.array([-13.3, 0.6, 0]), color=SILVER, stroke_width=1.6),
            Line(np.array([-6.3, -1.95, 0]), np.array([-6.3, -0.55, 0]), color=SILVER, stroke_width=1.4),
            Line(np.array([-12.7, -2.1, 0]), np.array([-12.7, -2.55, 0]), color=SILVER, stroke_width=1.3),
            Line(np.array([-6.9, -2.1, 0]), np.array([-6.9, -2.55, 0]), color=SILVER, stroke_width=1.3),
        )
        pillow = RoundedRectangle(width=1.55, height=0.65, corner_radius=0.28, color=SILVER, stroke_width=1.0, fill_color=SILVER, fill_opacity=0.05).move_to(np.array([-12.0, -0.95, 0]))
        patient_head = Circle(radius=0.38, color=PALE_GOLD, stroke_width=1.2, stroke_opacity=0.9).move_to(np.array([-11.8, -0.65, 0]))
        patient_body = polyline([
            np.array([-11.45, -0.85, 0]),
            np.array([-10.2, -1.1, 0]),
            np.array([-8.25, -1.1, 0]),
            np.array([-7.15, -1.55, 0]),
        ], color=SILVER, width=1.8, opacity=0.78)
        blanket = Polygon(
            np.array([-10.5, -0.88, 0]),
            np.array([-7.0, -1.02, 0]),
            np.array([-6.75, -1.82, 0]),
            np.array([-10.55, -1.82, 0]),
            color=BLUE,
            stroke_width=1.0,
            stroke_opacity=0.55,
            fill_color=AJOU_BLUE,
            fill_opacity=0.08,
        )
        patient = VGroup(pillow, patient_head, patient_body, blanket)

        monitor = RoundedRectangle(width=5.6, height=2.25, corner_radius=0.22, color=SKY, stroke_width=1.2, stroke_opacity=0.7, fill_color=BG_2, fill_opacity=0.46).move_to(np.array([-9.8, 2.15, 0]))
        irregular = polyline([
            np.array([-12.1 + i * 0.19, 2.15 + (0.12 * math.sin(i * 0.65) + (0.8 if i % 17 == 0 else -0.55 if i % 17 == 1 else 0.0)), 0])
            for i in range(25)
        ], color=GOLD, width=1.8, opacity=0.9)
        stable = polyline([
            np.array([-12.1 + i * 0.19, 2.15 + (0.10 * math.sin(i * 0.7) + (0.62 if i % 10 == 0 else -0.35 if i % 10 == 1 else 0.0)), 0])
            for i in range(25)
        ], color=CYAN, width=1.8, opacity=0.9)

        iv_pole = VGroup(
            Line(np.array([-14.0, -0.8, 0]), np.array([-14.0, 3.0, 0]), color=SILVER, stroke_width=1.2),
            Line(np.array([-14.0, 3.0, 0]), np.array([-13.35, 3.0, 0]), color=SILVER, stroke_width=1.0),
            RoundedRectangle(width=0.75, height=1.05, corner_radius=0.14, color=SKY, stroke_width=1.0, fill_color=SKY, fill_opacity=0.05).move_to(np.array([-13.2, 2.55, 0])),
            Line(np.array([-13.2, 2.0, 0]), np.array([-12.3, 0.1, 0]), color=CYAN, stroke_width=0.8, stroke_opacity=0.65),
        )
        iv_drop_path = Line(np.array([-13.2, 2.8, 0]), np.array([-13.2, 2.25, 0]), color=CYAN, stroke_width=0.6)
        iv_drop = Dot(iv_drop_path.get_start(), radius=0.05, color=CYAN)

        care_center = np.array([-9.8, -1.0, 0])
        care_rings = VGroup(*[Circle(radius=1.2 + i * 0.62, color=GOLD if i == 1 else SKY, stroke_width=1.0, stroke_opacity=0.25 - i * 0.035).move_to(care_center) for i in range(4)])
        caregiver_a = make_person(np.array([-5.0, 0.8, 0]), 1.3, color=GOLD)
        caregiver_b = make_person(np.array([-4.0, -1.0, 0]), 1.0, color=SKY)
        caregiver_target = np.array([-6.1, -0.4, 0])

        handover_nodes = VGroup()
        handover_links = VGroup()
        handover_pts = [np.array([1.0 + i * 2.55, 1.8 * math.sin(i * 0.85), 0]) for i in range(6)]
        for i, p in enumerate(handover_pts):
            handover_nodes.add(Circle(radius=0.34, color=GOLD if i in (0, 5) else SKY, stroke_width=1.2, stroke_opacity=0.75).move_to(p))
            if i < len(handover_pts) - 1:
                handover_links.add(polyline([p, (p + handover_pts[i + 1]) / 2 + UP * 0.45 * (-1) ** i, handover_pts[i + 1]], color=BLUE, width=1.0, opacity=0.5))
        handover_path = polyline(handover_pts, color=SKY, width=0.01, opacity=0.01)
        handover_token = Square(side_length=0.2, stroke_width=0, fill_color=PALE_GOLD, fill_opacity=1.0).move_to(handover_pts[0])

        group = VGroup(bed_frame, patient, monitor, irregular, iv_pole, iv_drop, care_rings, caregiver_a, caregiver_b, handover_nodes, handover_links, handover_token)
        self.play(
            LaggedStart(Create(bed_frame), FadeIn(patient), GrowFromCenter(monitor), Create(irregular), Create(iv_pole), FadeIn(iv_drop), GrowFromCenter(care_rings), FadeIn(caregiver_a), FadeIn(caregiver_b), Create(handover_links), FadeIn(handover_nodes), FadeIn(handover_token), lag_ratio=0.06),
            run_time=1.0,
        )
        self.play(
            Transform(irregular, stable),
            caregiver_a.animate.move_to(caregiver_target).scale(0.92),
            caregiver_b.animate.shift(RIGHT * 0.7 + UP * 0.3),
            care_rings.animate(rate_func=there_and_back).scale(1.32).set_stroke(opacity=0.07),
            patient_head.animate(rate_func=there_and_back).scale(1.22),
            MoveAlongPath(iv_drop, iv_drop_path, rate_func=linear),
            MoveAlongPath(handover_token, handover_path, rate_func=linear),
            LaggedStart(*[n.animate(rate_func=there_and_back).scale(1.45) for n in handover_nodes], lag_ratio=0.12),
            run_time=4.35,
        )
        self.transition_out(group, mode=1, direction=-1)

    # ------------------------------------------------------------------
    # 9. Business — decisions, value flows, analytics, market network.
    # ------------------------------------------------------------------
    def chapter_business(self) -> None:
        roots = [np.array([-14.6, y, 0]) for y in (-2.4, -0.8, 0.8, 2.4)]
        branch_paths = []
        branches = VGroup()
        tokens = VGroup()
        ends = [np.array([-5.3, y, 0]) for y in (2.3, -1.5, 1.2, -2.2)]
        for i, (s, e) in enumerate(zip(roots, ends)):
            pts = [s, np.array([-11.3, 0.6 * (-1) ** i, 0]), np.array([-8.3, -0.55 * (-1) ** i, 0]), e]
            p = polyline(pts, color=GOLD if i in (0, 3) else SKY, width=1.35, opacity=0.68)
            branch_paths.append(p)
            branches.add(p)
            tokens.add(Dot(s, radius=0.085, color=PALE_GOLD if i in (0, 3) else CYAN))

        bars = VGroup()
        target_bars = VGroup()
        heights = (1.2, 2.5, 1.8, 3.4, 2.8, 4.1, 3.3, 4.6, 4.0)
        for i, h in enumerate(heights):
            b = Rectangle(width=0.48, height=0.18, stroke_width=0, fill_color=SKY if i % 3 else GOLD, fill_opacity=0.72).move_to(np.array([-3.9 + i * 0.95, -2.5, 0]), aligned_edge=DOWN)
            bars.add(b)
            tb = Rectangle(width=0.48, height=h, stroke_width=0, fill_color=SKY if i % 3 else GOLD, fill_opacity=0.72).move_to(np.array([-3.9 + i * 0.95, -2.5, 0]), aligned_edge=DOWN)
            target_bars.add(tb)
        graph = polyline([np.array([-4.0 + i * 0.95, -1.8 + 0.66 * heights[i], 0]) for i in range(len(heights))], color=WHITE, width=1.2, opacity=0.72)

        nodes, edges, pts = make_node_network(np.array([10.5, 0, 0]), 3.25, 25, 13, node_color=GOLD, edge_color=SKY, connection_steps=(1, 3, 6))
        market = VGroup(edges, nodes)
        exchange_paths = VGroup()
        exchange_tokens = VGroup()
        epaths = []
        for i in range(5):
            a = 2 * PI * i / 5
            b = 2 * PI * ((i + 2) % 5) / 5
            p = polyline([
                np.array([10.5 + 2.7 * math.cos(a), 2.7 * math.sin(a), 0]),
                np.array([10.5, 0, 0]),
                np.array([10.5 + 2.7 * math.cos(b), 2.7 * math.sin(b), 0]),
            ], color=BLUE, width=0.8, opacity=0.32)
            exchange_paths.add(p)
            epaths.append(p)
            exchange_tokens.add(Square(side_length=0.17, stroke_width=0, fill_color=CYAN if i % 2 else PALE_GOLD, fill_opacity=0.95).move_to(p.get_start()))

        group = VGroup(branches, tokens, bars, graph, market, exchange_paths, exchange_tokens)
        self.play(
            LaggedStart(Create(branches), FadeIn(tokens), FadeIn(bars), Create(graph), FadeIn(market), Create(exchange_paths), FadeIn(exchange_tokens), lag_ratio=0.08),
            run_time=1.0,
        )
        self.play(
            *[MoveAlongPath(t, p, rate_func=linear) for t, p in zip(tokens, branch_paths)],
            Transform(bars, target_bars),
            graph.animate.shift(UP * 0.75).scale(1.03),
            Rotate(market, angle=PI * 0.72, rate_func=there_and_back),
            nodes.animate(rate_func=there_and_back).scale(1.4),
            *[MoveAlongPath(t, p, rate_func=linear) for t, p in zip(exchange_tokens, epaths)],
            run_time=4.2,
        )
        self.transition_out(group, mode=2, direction=1)

    # ------------------------------------------------------------------
    # 10. Social sciences — people, institutions, psychology, collective motion.
    # ------------------------------------------------------------------
    def chapter_social_sciences(self) -> None:
        people = VGroup()
        positions = [
            (-13.3, 2.2), (-11.5, 2.7), (-9.8, 1.9),
            (-13.8, 0.0), (-11.7, 0.5), (-9.7, -0.1),
            (-13.1, -2.2), (-11.0, -2.5), (-9.1, -1.8),
        ]
        for i, (x, y) in enumerate(positions):
            people.add(make_person(np.array([x, y, 0]), 0.85 + 0.08 * (i % 3), color=GOLD if i in (1, 4, 7) else SKY))
        social_links = VGroup()
        centers = [p.get_center() for p in people]
        for i in range(len(centers) - 1):
            social_links.add(Line(centers[i], centers[(i + 3) % len(centers)], color=BLUE, stroke_width=0.75, stroke_opacity=0.3))

        institution = VGroup(
            Polygon(np.array([-1.9, 1.45, 0]), np.array([0, 2.6, 0]), np.array([1.9, 1.45, 0]), color=SILVER, stroke_width=1.2, stroke_opacity=0.75),
            Rectangle(width=4.0, height=0.25, color=SILVER, stroke_width=0, fill_color=SILVER, fill_opacity=0.35).move_to(np.array([0, 1.35, 0])),
            *[Rectangle(width=0.35, height=2.4, color=SKY, stroke_width=1.0, fill_color=SKY, fill_opacity=0.025).move_to(np.array([x, 0.0, 0])) for x in (-1.35, -0.45, 0.45, 1.35)],
            Rectangle(width=4.25, height=0.28, color=SILVER, stroke_width=0, fill_color=SILVER, fill_opacity=0.35).move_to(np.array([0, -1.35, 0])),
        )
        policy_ripples = VGroup(*[Circle(radius=0.65 + i * 0.63, color=GOLD if i == 1 else SKY, stroke_width=1.0, stroke_opacity=0.26 - i * 0.03).move_to(ORIGIN) for i in range(5)])

        attractor_paths = VGroup()
        attractor_dots = VGroup()
        apaths = []
        for i in range(7):
            pts = [
                np.array([7.1 + 7.0 * t, 2.4 * math.sin(2 * PI * t + i * 0.75) * (1 - 0.35 * t), 0])
                for t in np.linspace(0, 1, 110)
            ]
            p = polyline(pts, color=CYAN if i % 2 else BLUE, width=0.85, opacity=0.34)
            attractor_paths.add(p)
            apaths.append(p)
            attractor_dots.add(Dot(p.get_start(), radius=0.055 + 0.008 * (i % 3), color=GOLD if i == 3 else SKY))

        sport_path = polyline([np.array([6.8 + 8.0 * t, -3.0 + 1.25 * math.sin(PI * t) + 0.3 * math.sin(6 * PI * t), 0]) for t in np.linspace(0, 1, 120)], color=GOLD, width=1.4, opacity=0.75)
        athlete = Dot(sport_path.get_start(), radius=0.11, color=PALE_GOLD)

        group = VGroup(people, social_links, institution, policy_ripples, attractor_paths, attractor_dots, sport_path, athlete)
        self.play(
            LaggedStart(FadeIn(people), Create(social_links), Create(institution), GrowFromCenter(policy_ripples), Create(attractor_paths), FadeIn(attractor_dots), Create(sport_path), FadeIn(athlete), lag_ratio=0.07),
            run_time=1.0,
        )
        self.play(
            people.animate(rate_func=there_and_back).arrange_in_grid(rows=3, cols=3, buff=(0.95, 0.55)).move_to(np.array([-11.4, 0, 0])),
            social_links.animate(rate_func=there_and_back).rotate(PI / 6, about_point=np.array([-11.4, 0, 0])),
            institution.animate(rate_func=there_and_back).shift(UP * 0.3).scale(1.06),
            policy_ripples.animate(rate_func=there_and_back).scale(1.5).set_stroke(opacity=0.06),
            *[MoveAlongPath(d, p, rate_func=linear) for d, p in zip(attractor_dots, apaths)],
            MoveAlongPath(athlete, sport_path, rate_func=ease_in_out_sine),
            run_time=4.3,
        )
        self.transition_out(group, mode=0, direction=-1)

    # ------------------------------------------------------------------
    # 11. Humanities — book, language gesture, memory, media timeline.
    # ------------------------------------------------------------------
    def chapter_humanities(self) -> None:
        book_left = Polygon(np.array([-14.2, 2.6, 0]), np.array([-9.8, 1.8, 0]), np.array([-9.8, -2.7, 0]), np.array([-14.2, -1.8, 0]), color=SKY, stroke_width=1.3, stroke_opacity=0.72, fill_color=BLUE, fill_opacity=0.035)
        book_right = Polygon(np.array([-9.8, 1.8, 0]), np.array([-5.4, 2.6, 0]), np.array([-5.4, -1.8, 0]), np.array([-9.8, -2.7, 0]), color=GOLD, stroke_width=1.3, stroke_opacity=0.72, fill_color=GOLD, fill_opacity=0.025)
        spine = Line(np.array([-9.8, 1.8, 0]), np.array([-9.8, -2.7, 0]), color=SILVER, stroke_width=1.1)
        page_lines = VGroup()
        for i in range(6):
            y = 1.65 - i * 0.65
            page_lines.add(Line(np.array([-13.55, y, 0]), np.array([-10.55, y - 0.2, 0]), color=SILVER, stroke_width=0.75, stroke_opacity=0.45))
            page_lines.add(Line(np.array([-9.05, y - 0.2, 0]), np.array([-6.05, y, 0]), color=SILVER, stroke_width=0.75, stroke_opacity=0.45))
        page_turn = Polygon(np.array([-9.75, 1.75, 0]), np.array([-6.0, 2.35, 0]), np.array([-7.1, -1.9, 0]), np.array([-9.75, -2.55, 0]), color=WHITE, stroke_width=1.0, stroke_opacity=0.55, fill_color=SKY, fill_opacity=0.035)
        book = VGroup(book_left, book_right, spine, page_lines, page_turn)

        strokes = VGroup(
            polyline([np.array([-4.3, 2.6, 0]), np.array([-2.8, 0.8, 0]), np.array([-3.7, -2.4, 0])], color=WHITE, width=2.1),
            Arc(radius=1.55, start_angle=PI * 0.15, angle=PI * 1.65, color=GOLD, stroke_width=1.9).move_to(np.array([-0.5, 0.1, 0])),
            polyline([np.array([1.2, 2.4, 0]), np.array([2.8, 1.0, 0]), np.array([1.5, -0.2, 0]), np.array([3.0, -2.4, 0])], color=CYAN, width=1.8),
            Line(np.array([-3.5, -2.9, 0]), np.array([3.4, -2.9, 0]), color=BLUE, stroke_width=1.0, stroke_opacity=0.5),
        )
        voice_a = make_wave(-4.5, 4.2, 0.0, 0.72, 5.8, SKY, width=1.2)
        voice_b = make_wave(-4.5, 4.2, 0.0, 1.28, 2.4, GOLD, width=1.7, phase=1.1)

        timeline = Line(np.array([5.4, 0, 0]), np.array([14.8, 0, 0]), color=SILVER, stroke_width=1.1, stroke_opacity=0.55)
        frames = VGroup()
        moments = VGroup()
        for i, x in enumerate(np.linspace(6.0, 14.2, 7)):
            moments.add(Dot(np.array([x, 0, 0]), radius=0.065, color=GOLD if i in (0, 6) else SKY))
            f = Rectangle(width=0.9, height=1.35, color=BLUE, stroke_width=0.9, stroke_opacity=0.55, fill_color=SKY, fill_opacity=0.025).move_to(np.array([x, 1.25 * (-1) ** i, 0]))
            f.add(Line(f.get_corner(LEFT + UP) + RIGHT * 0.15 + DOWN * 0.22, f.get_corner(RIGHT + DOWN) + LEFT * 0.15 + UP * 0.22, color=GOLD if i % 3 == 0 else SKY, stroke_width=0.8, stroke_opacity=0.45))
            frames.add(f)

        group = VGroup(book, strokes, voice_a, timeline, moments, frames)
        self.play(
            LaggedStart(Create(book), LaggedStart(*[Create(s) for s in strokes], lag_ratio=0.12), Create(voice_a), Create(timeline), FadeIn(moments), FadeIn(frames), lag_ratio=0.08),
            run_time=1.05,
        )
        self.play(
            page_turn.animate(rate_func=there_and_back).apply_matrix([[-0.15, 0.45], [0.0, 1.0]]).shift(RIGHT * 1.5),
            LaggedStart(*[s.animate(rate_func=there_and_back).shift(np.array([0.35 * math.sin(i), 0.45 * math.cos(i), 0])).rotate(PI / 5 * (-1) ** i) for i, s in enumerate(strokes)], lag_ratio=0.1),
            Transform(voice_a, voice_b),
            LaggedStart(*[f.animate(rate_func=there_and_back).shift(UP * 0.55 * (-1) ** i).rotate(PI / 14 * (-1) ** i) for i, f in enumerate(frames)], lag_ratio=0.08),
            moments.animate(rate_func=there_and_back).scale(1.5),
            run_time=4.2,
        )
        self.transition_out(group, mode=1, direction=1)

    # ------------------------------------------------------------------
    # 12. International studies — globe, exchange arcs, regional connections.
    # ------------------------------------------------------------------
    def chapter_international(self) -> None:
        globe = VGroup(
            Circle(radius=2.8, color=SKY, stroke_width=1.4, stroke_opacity=0.72),
            Ellipse(width=2.0, height=5.6, color=BLUE, stroke_width=0.9, stroke_opacity=0.45),
            Ellipse(width=4.0, height=5.6, color=BLUE, stroke_width=0.9, stroke_opacity=0.45),
            Ellipse(width=5.6, height=1.8, color=BLUE, stroke_width=0.9, stroke_opacity=0.45),
            Ellipse(width=5.6, height=3.7, color=BLUE, stroke_width=0.9, stroke_opacity=0.45),
        )
        hubs = VGroup(*[Dot(np.array([x, y, 0]), radius=0.09, color=GOLD) for x, y in ((-1.7, 0.8), (1.4, 1.4), (1.75, -0.75), (-0.9, -1.65), (0.2, 0.15))])
        globe_group = VGroup(globe, hubs)

        paths = VGroup()
        tokens = VGroup()
        path_list = []
        specs = [
            (np.array([-15.0, 2.8, 0]), np.array([15.0, -1.8, 0]), GOLD),
            (np.array([-15.0, 0.8, 0]), np.array([15.0, 2.6, 0]), SKY),
            (np.array([-15.0, -1.3, 0]), np.array([15.0, 0.4, 0]), CYAN),
            (np.array([-15.0, -3.0, 0]), np.array([15.0, -2.8, 0]), VIOLET),
        ]
        for i, (s, e, c) in enumerate(specs):
            pts = [s, np.array([-7.5, -0.8 * s[1], 0]), np.array([0, 0.5 * (-1) ** i, 0]), np.array([7.5, -0.6 * e[1], 0]), e]
            p = polyline(pts, color=c, width=1.25, opacity=0.55)
            paths.add(p)
            path_list.append(p)
            token = VGroup(
                Square(side_length=0.18, stroke_width=0, fill_color=c, fill_opacity=0.9),
                Circle(radius=0.12, color=WHITE, stroke_width=0.8, stroke_opacity=0.65),
            ).move_to(s)
            tokens.add(token)

        ports = VGroup()
        for side in (-1, 1):
            for i in range(4):
                x = side * (9.0 + i * 1.4)
                ports.add(make_hex(np.array([x, -3.2 + i * 2.05, 0]), 0.32, GOLD if i % 2 == 0 else SKY, opacity=0.62, fill_opacity=0.05))

        group = VGroup(paths, tokens, ports, globe_group)
        self.play(
            LaggedStart(Create(paths), FadeIn(tokens), FadeIn(ports), GrowFromCenter(globe_group), lag_ratio=0.08),
            run_time=1.0,
        )
        self.play(
            *[MoveAlongPath(t, p, rate_func=linear) for t, p in zip(tokens, path_list)],
            Rotate(globe, angle=PI * 0.9, rate_func=there_and_back),
            hubs.animate(rate_func=there_and_back).scale(1.75),
            ports.animate(rate_func=there_and_back).rotate(PI / 3).scale(1.25),
            run_time=4.15,
        )
        self.transition_out(group, mode=2, direction=-1)

    # ------------------------------------------------------------------
    # 13. Dasan / open major — exploration, branching, self-designed path.
    # ------------------------------------------------------------------
    def chapter_open_major(self) -> None:
        origin = np.array([-14.7, 0, 0])
        ends = [np.array([14.5, y, 0]) for y in (3.2, 1.6, 0, -1.6, -3.2)]
        paths = VGroup()
        path_list = []
        explorers = VGroup()
        for i, e in enumerate(ends):
            pts = [
                origin,
                np.array([-10.8, 0, 0]),
                np.array([-6.2, (i - 2) * 0.35, 0]),
                np.array([-1.5, (i - 2) * 0.9, 0]),
                np.array([4.1, (i - 2) * 1.05 + 0.45 * math.sin(i), 0]),
                np.array([9.5, e[1] * 0.78, 0]),
                e,
            ]
            color = GOLD if i == 2 else SKY
            p = polyline(pts, color=color, width=2.0 if i == 2 else 1.05, opacity=0.84 if i == 2 else 0.34)
            paths.add(p)
            path_list.append(p)
            explorers.add(Dot(origin, radius=0.13 if i == 2 else 0.075, color=PALE_GOLD if i == 2 else CYAN))

        decision_nodes = VGroup(*[Circle(radius=0.33, color=GOLD if i == 2 else SKY, stroke_width=1.1, stroke_opacity=0.75).move_to(e) for i, e in enumerate(ends)])
        intermediate_nodes = VGroup()
        for x in (-10.8, -6.2, -1.5, 4.1, 9.5):
            for y in (-2.2, 0, 2.2):
                intermediate_nodes.add(make_hex(np.array([x, y, 0]), 0.18, BLUE, opacity=0.35))

        chosen_mesh_nodes, chosen_mesh_edges, _ = make_node_network(np.array([8.5, 0, 0]), 3.2, 20, 88, node_color=GOLD, edge_color=SKY, connection_steps=(1, 4))
        chosen_mesh = VGroup(chosen_mesh_edges, chosen_mesh_nodes).set_opacity(0)
        group = VGroup(paths, explorers, decision_nodes, intermediate_nodes, chosen_mesh)
        self.play(
            LaggedStart(Create(paths), FadeIn(explorers), GrowFromCenter(decision_nodes), FadeIn(intermediate_nodes), lag_ratio=0.08),
            run_time=1.0,
        )
        self.play(
            *[MoveAlongPath(d, p, rate_func=ease_in_out_sine) for d, p in zip(explorers, path_list)],
            decision_nodes.animate(rate_func=there_and_back).scale(1.45),
            paths[2].animate.set_stroke(width=3.5, opacity=1.0),
            chosen_mesh.animate.set_opacity(1).scale(1.05),
            Rotate(chosen_mesh, angle=PI * 0.65, rate_func=there_and_back),
            run_time=4.15,
        )
        # Do not fully clear: these branches fracture into the final logo assembly.
        self.open_major_group = group

    # ------------------------------------------------------------------
    # 14. Final logo assembly — geometric fragments converge into exact symbol.
    # ------------------------------------------------------------------
    def chapter_logo_assembly(self) -> None:
        previous = getattr(self, "open_major_group", VGroup())

        # Collapse the chosen paths into a broad central vortex.
        vortex = VGroup()
        for i in range(10):
            r = 1.0 + i * 0.6
            a = Arc(radius=r, start_angle=PI * (0.12 + i * 0.03), angle=PI * (1.4 + 0.05 * i), color=GOLD if i in (2, 7) else SKY, stroke_width=0.9 + 0.1 * (i % 3), stroke_opacity=0.28)
            a.stretch(1.55, 0)
            vortex.add(a)

        # Sample geometric tile targets from the supplied symbol mask.
        mask = Image.open(LOGO_PATH).convert("RGBA")
        alpha = np.array(mask)[:, :, 3]
        h, w = alpha.shape
        samples: list[tuple[float, float]] = []
        step = 14
        for yy in range(step // 2, h, step):
            for xx in range(step // 2, w, step):
                window = alpha[max(0, yy - step // 3):min(h, yy + step // 3 + 1), max(0, xx - step // 3):min(w, xx + step // 3 + 1)]
                if window.mean() > 75:
                    samples.append((xx, yy))

        logo_height = 5.8
        scale = logo_height / h
        rng = np.random.default_rng(909)
        tiles = VGroup()
        targets = VGroup()
        for i, (xx, yy) in enumerate(samples):
            tx = (xx - w / 2) * scale
            ty = (h / 2 - yy) * scale
            start_side = i % 4
            if start_side == 0:
                start = np.array([-15.3, rng.uniform(-4.3, 4.3), 0])
            elif start_side == 1:
                start = np.array([15.3, rng.uniform(-4.3, 4.3), 0])
            elif start_side == 2:
                start = np.array([rng.uniform(-13.5, 13.5), 4.8, 0])
            else:
                start = np.array([rng.uniform(-13.5, 13.5), -4.8, 0])

            size = rng.uniform(0.12, 0.23)
            if i % 3 == 0:
                tile = Triangle(stroke_width=0, fill_color=GOLD if i % 11 == 0 else SKY, fill_opacity=rng.uniform(0.55, 0.95)).scale(size).move_to(start).rotate(rng.uniform(0, 2 * PI))
                target = tile.copy().move_to(np.array([tx, ty, 0])).rotate(rng.uniform(-PI, PI)).set_fill(WHITE, opacity=0.96)
            else:
                tile = Square(side_length=size, stroke_width=0, fill_color=GOLD if i % 13 == 0 else SKY, fill_opacity=rng.uniform(0.55, 0.95)).move_to(start).rotate(rng.uniform(0, PI))
                target = tile.copy().move_to(np.array([tx, ty, 0])).rotate(rng.uniform(-PI / 2, PI / 2)).set_fill(WHITE, opacity=0.96)
            tiles.add(tile)
            targets.add(target)

        logo = ImageMobject(str(LOGO_PATH))
        logo.set_height(logo_height)

        halo = VGroup(
            Circle(radius=3.35, color=SKY, stroke_width=1.1, stroke_opacity=0.18),
            Circle(radius=4.1, color=BLUE, stroke_width=0.8, stroke_opacity=0.12),
            Circle(radius=4.9, color=GOLD, stroke_width=0.7, stroke_opacity=0.07),
        )
        rays = VGroup()
        for i in range(32):
            a = 2 * PI * i / 32
            r0 = 3.0 + 0.4 * (i % 3)
            r1 = 7.0 + 1.2 * (i % 4)
            rays.add(Line(np.array([r0 * math.cos(a), r0 * math.sin(a), 0]), np.array([r1 * math.cos(a), r1 * math.sin(a), 0]), color=GOLD if i % 7 == 0 else SKY, stroke_width=0.7, stroke_opacity=0.18))

        logo.set_z_index(30)
        tiles.set_z_index(20)
        halo.set_z_index(5)
        rays.set_z_index(4)
        vortex.set_z_index(10)
        self.add(vortex, tiles, halo, rays)
        self.play(
            previous.animate.scale(0.15).rotate(PI / 2).set_opacity(0).move_to(ORIGIN),
            LaggedStart(*[Create(a) for a in vortex], lag_ratio=0.04),
            FadeIn(halo, scale=0.7),
            FadeIn(rays),
            run_time=1.1,
        )
        self.remove(previous)

        tile_anims: list[Animation] = []
        for i, (tile, target) in enumerate(zip(tiles, targets)):
            arc = (PI / 2) * (-1 if i % 2 else 1) * (0.35 + 0.12 * (i % 3))
            tile_anims.append(Transform(tile, target, path_arc=arc, rate_func=ease_in_out_sine))

        self.play(
            LaggedStart(*tile_anims, lag_ratio=0.008),
            Rotate(vortex, angle=PI * 1.35, rate_func=linear),
            halo.animate.scale(0.78).set_stroke(opacity=0.08),
            rays.animate.scale(0.75).set_stroke(opacity=0.05),
            run_time=3.8,
        )

        self.play(
            FadeIn(logo, scale=0.94),
            FadeOut(tiles, scale=0.96),
            FadeOut(vortex, scale=0.35),
            FadeOut(rays),
            halo.animate.scale(1.08).set_stroke(opacity=0.15),
            run_time=1.25,
        )
        self.play(
            logo.animate(rate_func=there_and_back).scale(1.035),
            halo.animate(rate_func=there_and_back).scale(1.12),
            run_time=1.35,
        )
        self.wait(0.45)


if __name__ == "__main__":
    pass