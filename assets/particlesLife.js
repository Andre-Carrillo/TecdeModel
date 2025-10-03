// sketch.js
// Particles Life with cyclic world + spatial partitioning (uniform grid)

let circles = [];
let n_circles = 1000;
let seed = 2;
let n_classes = 6;

let half_t = 0.05;
let circlesRadius = 0.007;
let force_factor = 10.0;
let matrix_inverse_amplification = 2.0;
let max_distance_interaction = 0.15; // in normalized coordinates
let delta_t = 0.02;
let cri_distance = 0.3;

let interaction_matrix = [];
let rng;

// grid
let gridSize;       // side of each cell
let nCells;         // number of cells per axis
let grid;           // 2D array of cells

function seededRandom(s) {
  let m = 0x80000000, a = 1103515245, c = 12345;
  let state = s % m;
  return function() {
    state = (a * state + c) % m;
    return state / (m - 1);
  };
}

class Circle {
  constructor(r, pos, vel, classification = 0) {
    this.radius = r;
    this.position = pos.copy();
    this.velocity = vel.copy();
    this.acceleration = createVector(0, 0);
    this.mass = 1.0;
    this.classification = classification;
  }

  update(dt) {
    let decay = Math.exp(-Math.log(2.0) * (dt / half_t));
    this.velocity.mult(decay);
    this.velocity.add(p5.Vector.mult(this.acceleration, dt));
    this.position.add(p5.Vector.mult(this.velocity, dt));

    // wrap cyclically
    if (this.position.x > 1.0) this.position.x -= 2.0;
    if (this.position.x < -1.0) this.position.x += 2.0;
    if (this.position.y > 1.0) this.position.y -= 2.0;
    if (this.position.y < -1.0) this.position.y += 2.0;
  }
}

// cyclic difference
function cyclicDiff(a, b) {
  let dx = b.x - a.x;
  let dy = b.y - a.y;
  if (dx > 1.0) dx -= 2.0;
  if (dx < -1.0) dx += 2.0;
  if (dy > 1.0) dy -= 2.0;
  if (dy < -1.0) dy += 2.0;
  return createVector(dx, dy);
}

// force law
function getForceMagnitude(r, m) {
  if (r < cri_distance) {
    return (r / cri_distance - 1) * force_factor;
  } else if (r < 1.0) {
    return m * (1 - Math.abs(2 * r - 1 - cri_distance) / (1 - cri_distance)) * force_factor;
  } else {
    return 0.0;
  }
}

// grid helpers
function initGrid() {
  gridSize = max_distance_interaction;   // side length of cell
  nCells = Math.ceil(2.0 / gridSize);    // from -1..1
  grid = Array.from({ length: nCells }, () =>
    Array.from({ length: nCells }, () => [])
  );
}

function cellIndex(pos) {
  let x = Math.floor((pos.x + 1.0) / 2.0 * nCells);
  let y = Math.floor((pos.y + 1.0) / 2.0 * nCells);
  x = (x + nCells) % nCells;
  y = (y + nCells) % nCells;
  return { x, y };
}

function populateGrid() {
  for (let i = 0; i < nCells; i++) {
    for (let j = 0; j < nCells; j++) {
      grid[i][j] = [];
    }
  }
  for (let c of circles) {
    let { x, y } = cellIndex(c.position);
    grid[x][y].push(c);
  }
}

function computeForces() {
  for (let c of circles) c.acceleration.set(0, 0);

  for (let i = 0; i < nCells; i++) {
    for (let j = 0; j < nCells; j++) {
      let cellParticles = grid[i][j];
      if (cellParticles.length === 0) continue;

      for (let ci of cellParticles) {
        // check this cell and 8 neighbors
        for (let di = -1; di <= 1; di++) {
          for (let dj = -1; dj <= 1; dj++) {
            let ni = (i + di + nCells) % nCells;
            let nj = (j + dj + nCells) % nCells;
            let neighborParticles = grid[ni][nj];

            for (let cj of neighborParticles) {
              if (ci === cj) continue;
              let diff = cyclicDiff(ci.position, cj.position);
              let distance = diff.mag();
              if (distance > 0 && distance < max_distance_interaction) {
                let direction = diff.copy().normalize();
                let normalized_distance = distance / max_distance_interaction;
                let m = interaction_matrix[ci.classification][cj.classification];
                let force = getForceMagnitude(normalized_distance, m);
                ci.acceleration.add(direction.mult((force * max_distance_interaction) / ci.mass));
              }
            }
          }
        }
      }
    }
  }
}

function normToScreen(pos) {
  return createVector(
    (pos.x * 0.5 + 0.5) * width,
    (1 - (pos.y * 0.5 + 0.5)) * height
  );
}

function setup() {
  let canvas = createCanvas(600, 400);
  canvas.parent("p5-canvas")
  pixelDensity(1);
  background(20);

  rng = seededRandom(seed);

  // interaction matrix
  interaction_matrix = new Array(n_classes);
  for (let i = 0; i < n_classes; i++) {
    interaction_matrix[i] = new Array(n_classes);
    for (let j = 0; j < n_classes; j++) {
      let val = (Math.floor(rng() * 20) / 10.0 - 1.0) / matrix_inverse_amplification;
      interaction_matrix[i][j] = val;
    }
  }

  // circles
  circles = [];
  for (let i = 0; i < n_circles; i++) {
    let px = (Math.floor(rng() * 200) - 100) / 100.0;
    let py = (Math.floor(rng() * 200) - 100) / 100.0;
    let pos = createVector(px, py);
    let vel = createVector(0, 0);
    let cls = Math.floor(rng() * n_classes);
    circles.push(new Circle(circlesRadius, pos, vel, cls));
  }

  initGrid();
  frameRate(60);
}

function draw() {
  fill(12, 12, 14, 255);
  noStroke();
  rect(0, 0, width, height);

  let dt = constrain(deltaTime / 1000.0, 1e-6, 0.05);

  populateGrid();
  computeForces();

  noStroke();
  for (let c of circles) {
    c.update(dt);

    let sPos = normToScreen(c.position);
    let pixelRadius = c.radius * Math.min(width, height) * 0.5;

    let col;
    switch (c.classification) {
      case 0: col = color(255, 130, 51); break;
      case 1: col = color(51, 153, 255); break;
      case 2: col = color(204, 25, 77); break;
      case 3: col = color(51, 204, 77); break;
      case 4: col = color(153, 77, 204); break;
      case 5: col = color(255, 255, 51); break;
      default: col = color(230);
    }
    fill(red(col), green(col), blue(col), 200);
    ellipse(sPos.x, sPos.y, pixelRadius * 2, pixelRadius * 2);
  }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}

