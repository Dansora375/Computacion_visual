void setup() {
  size(600, 600, P3D);  // Sketch en 3D
  noStroke();
}

void draw() {
  background(30);
  lights();  // Luz básica

  float t = millis() / 1000.0;  // Tiempo en segundos

  pushMatrix();

  // Movimiento ondulado (trayectoria senoidal en X y Z)
  float x = cos(t) * 100;
  float z = sin(t) * 100;
  translate(width/2 + x, height/2, z);

  // Rotación continua sobre X e Y
  rotateX(t);
  rotateY(t * 1.5);

  // Escalado suave y cíclico
  float s = 50 + sin(t * 2) * 20;
  scale(s / 50.0);  // Escalamos proporcional al tamaño base

  // Cubo
  fill(100, 180, 255);
  box(50);

  popMatrix();
}
