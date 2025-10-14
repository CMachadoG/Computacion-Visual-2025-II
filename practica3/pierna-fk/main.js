import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 1000);
camera.position.set(0, 2, 6);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);

// Iluminación
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 10, 5);
scene.add(light);
scene.add(new THREE.AmbientLight(0x404040));

// Clock para animación
const clock = new THREE.Clock();

// Materiales y geometrías
const material = new THREE.MeshStandardMaterial({ color: 0x88ccff });
const geoMuslo = new THREE.CylinderGeometry(0.15, 0.15, 3);
const geoPierna = new THREE.CylinderGeometry(0.12, 0.12, 3);

// Construcción de jerarquía
const cadera = new THREE.Object3D();
scene.add(cadera);

// Muslo
const muslo = new THREE.Mesh(geoMuslo, material);
muslo.position.y = -1.5; // mitad de 3
cadera.add(muslo);

// Rodilla
const rodilla = new THREE.Object3D();
rodilla.position.y = -1.5; // punto final del muslo
muslo.add(rodilla);

// Pierna
const pierna = new THREE.Mesh(geoPierna, material);
pierna.position.y = -1.5; // mitad de 3
rodilla.add(pierna);

// Pie
const pie = new THREE.Mesh(
  new THREE.BoxGeometry(1, 0.3, 1.5),
  new THREE.MeshStandardMaterial({ color: 0xff0000 })
);
pie.position.y = -1.5; // al final de la pierna
pierna.add(pie);

// Suelo
const suelo = new THREE.Mesh(
  new THREE.PlaneGeometry(20, 20),
  new THREE.MeshStandardMaterial({ color: 0x444444 })
);
suelo.rotation.x = -Math.PI / 2;
suelo.position.y = -6.3; // 🔽 mover el suelo debajo de la pierna
scene.add(suelo);

// Controles de cámara
const controls = new OrbitControls(camera, renderer.domElement);

// Animación
function animate() {
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();

  muslo.rotation.x = Math.sin(t) * 0.5;
  rodilla.rotation.x = Math.sin(t * 2) * 0.7;
  renderer.render(scene, camera);
}
animate();
