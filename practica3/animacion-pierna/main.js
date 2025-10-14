import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { gsap } from 'gsap';

// --- Escena y cámara ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101820);

const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 100);
camera.position.set(4, 3, 6);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// --- Luces ---
scene.add(new THREE.AmbientLight(0x404040, 1.2));
const dirLight = new THREE.DirectionalLight(0xffffff, 1.8);
dirLight.position.set(5, 10, 7);
scene.add(dirLight);

// --- Suelo ---
const floor = new THREE.Mesh(
  new THREE.PlaneGeometry(20, 20),
  new THREE.MeshStandardMaterial({ color: 0x222222 })
);
floor.rotation.x = -Math.PI / 2;
floor.position.y = -6.3
scene.add(floor);

// --- Materiales ---
const metalMat = new THREE.MeshStandardMaterial({ color: 0xd1a054, metalness: 0.6, roughness: 0.4 });
const darkMat = new THREE.MeshStandardMaterial({ color: 0x444444 });

// --- Construcción de la pierna ---
const base = new THREE.Object3D();
scene.add(base);

// Cadera
const caderaMesh = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.3, 0.5), darkMat);
caderaMesh.position.y = 2.5;
base.add(caderaMesh);

// Muslo
const muslo = new THREE.Object3D();
muslo.position.y = 2.5;
base.add(muslo);
const musloMesh = new THREE.Mesh(new THREE.BoxGeometry(0.3, 1.8, 0.3), metalMat);
musloMesh.position.y = -0.9;
muslo.add(musloMesh);

// Rodilla
const rodilla = new THREE.Object3D();
rodilla.position.y = -1.8;
muslo.add(rodilla);

// Pierna inferior
const pierna = new THREE.Object3D();
rodilla.add(pierna);
const piernaMesh = new THREE.Mesh(new THREE.BoxGeometry(0.25, 1.5, 0.25), metalMat);
piernaMesh.position.y = -0.75;
pierna.add(piernaMesh);

// Tobillo
const tobillo = new THREE.Object3D();
tobillo.position.y = -1.5;
pierna.add(tobillo);

// Pie
const pieMesh = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.2, 1), darkMat);
pieMesh.position.set(0, -0.1, 0.3);
tobillo.add(pieMesh);

// Esfera (objetivo visual)
const bola = new THREE.Mesh(
  new THREE.SphereGeometry(0.15, 16, 16),
  new THREE.MeshStandardMaterial({ color: 0xff2222 })
);
bola.position.set(0, 0.3, 0.8);
scene.add(bola);

// --- Timeline de animación (30 segundos aprox) ---
const tl = gsap.timeline({ repeat: -1, defaults: { ease: "power2.inOut" } });

// Principio: anticipación y “slow in/out”
tl.to(muslo.rotation, { x: 0.4, duration: 1.5 })
  .to(rodilla.rotation, { x: -0.8, duration: 1.5 }, "<0.1")
  .to(tobillo.rotation, { x: 0.2, duration: 1.5 }, "<0.2")
  .to(bola.position, { z: "+=2", duration: 0.8, ease: "power3.out" }, "<0.25")
  // Movimiento de estiramiento
  .to(muslo.rotation, { x: -0.2, duration: 1.8, ease: "elastic.out(1, 0.4)" })
  .to(rodilla.rotation, { x: 0.5, duration: 1.8, ease: "elastic.out(1, 0.4)" }, "<")
  // Rebote (principio: squash & stretch)
  .to(muslo.rotation, { x: 0.1, duration: 0.6, ease: "power2.inOut" })
  .to(rodilla.rotation, { x: -0.2, duration: 0.6, ease: "power2.inOut" }, "<")
  // Caminata simulada
  .to(base.position, { z: "+=0.5", duration: 2 }, "<") // avance pequeño de la pierna
  .to(bola.position, { z: "+=1.5", duration: 2 }, "<")
  .to(muslo.rotation, { x: -0.5, duration: 1.5 })
  .to(rodilla.rotation, { x: 0.7, duration: 1.5 }, "<")
  .to(tobillo.rotation, { x: -0.3, duration: 1.5 }, "<")
  // Retorno suave (principio: arco, continuidad)
  .to(base.position, { x: 0, duration: 3, ease: "power1.inOut" })
  .to([muslo.rotation, rodilla.rotation, tobillo.rotation], { x: 0, duration: 2.5 }, "<");

// --- Animación principal ---
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
animate();
