void setup() {
  size(600, 600, P3D);  // 3D sketch window
  noStroke();           // Disable stroke for shapes
}

void draw() {
  background(30);       // Dark background
  lights();             // Enable default lighting

  float t = millis() / 1000.0;  // Time in seconds

  pushMatrix();         // Save the current transformation state

  // Wavy motion (sine wave path in X and Z)
  float x = cos(t) * 100;
  float z = sin(t) * 100;
  translate(width / 2 + x, height / 2, z);  // Move the cube in a circular path

  // Continuous rotation around X and Y axes
  rotateX(t);
  rotateY(t * 1.5);

  // Smooth cyclic scaling
  float s = 50 + sin(t * 2) * 20;  // Varies between 30 and 70
  scale(s / 50.0);  // Scale relative to base size

  // Draw the cube
  fill(100, 180, 255);  // Light blue color
  box(50);

  popMatrix();          // Restore the previous transformation state
}
