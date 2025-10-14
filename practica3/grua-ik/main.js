import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101820);

const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 100);
camera.position.set(6, 3, 8);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

scene.add(new THREE.AmbientLight(0x404040, 1.2));
const dirLight = new THREE.DirectionalLight(0xffffff, 1.8);
dirLight.position.set(5, 10, 7);
scene.add(dirLight);

// floor
const floor = new THREE.Mesh(new THREE.PlaneGeometry(30, 30), new THREE.MeshStandardMaterial({ color: 0x222222 }));
floor.rotation.x = -Math.PI / 2;
scene.add(floor);

// materials
const metalMat = new THREE.MeshStandardMaterial({ color: 0xd1a054, metalness: 0.6, roughness: 0.4 });
const darkMat = new THREE.MeshStandardMaterial({ color: 0x444444 });

// --- ESTRUCTURA: base -> poste -> brazo1 -> joint -> brazo2 -> joint2 -> brazo3 -> gancho
const base = new THREE.Object3D();
scene.add(base);
const baseMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.7, 0.3, 32), darkMat);
baseMesh.position.y = -0.15; // para que el base object3d quede arriba
base.add(baseMesh);

// poste
const poste = new THREE.Mesh(new THREE.BoxGeometry(0.4, 5, 0.4), metalMat);
poste.position.y = 2.5; // mitad de 3
base.add(poste);

// PARÁMETROS 
const L1 = 2.0;   // primer brazo length
const L2 = 1.5;   // segundo brazo length
const L3 = 1.5;   // tercer brazo length

// brazo1 
const brazo1 = new THREE.Object3D();
brazo1.position.y = 5; // tope del poste (poste altura 3 -> y=3)
base.add(brazo1);
const b1mesh = new THREE.Mesh(new THREE.BoxGeometry(0.3, L1, 0.3), metalMat);
b1mesh.position.y = L1 / 2; // mover mesh para que pivote quede en la base
brazo1.add(b1mesh);

// joint (en la punta del brazo1)
const joint = new THREE.Object3D();
joint.position.y = L1; // al final del primer brazo (en coordenadas locales de brazo1)
brazo1.add(joint);

// brazo2 (Object3D pivot en su base)
const brazo2 = new THREE.Object3D();
joint.add(brazo2);
const b2mesh = new THREE.Mesh(new THREE.BoxGeometry(0.25, L2, 0.25), metalMat);
b2mesh.position.y = L2 / 2;
brazo2.add(b2mesh);

// joint2 (en la punta del brazo2)
const joint2 = new THREE.Object3D();
joint2.position.y = L2;
brazo2.add(joint2);

// brazo3
const brazo3Mesh = new THREE.Mesh(new THREE.BoxGeometry(0.2, L3, 0.2), metalMat);
brazo3Mesh.position.y = L3 / 2;
joint2.add(brazo3Mesh);

// gancho al final de brazo3
const gancho = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.25, 0.25), new THREE.MeshStandardMaterial({ color: 0xff0000 }));
gancho.position.y = L3 + 0.15; // ligeramente por debajo del final
joint2.add(gancho);

// target
const target = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 16), new THREE.MeshStandardMaterial({ color: 0xff2222 }));
scene.add(target);

// interacción
let targetPos = new THREE.Vector2(2.0, 1.0);

// EVENTO MOUSE
window.addEventListener('mousemove', (e) => {
  const x = (e.clientX / innerWidth) * 6 - 3;
  const y = (1 - e.clientY / innerHeight) * 4 - 1;
  targetPos.set(x, y);
});

// IK: enfoque práctico para 3 segmentos (resolvemos 2 primeros para alcanzar "punto cercano" al objetivo, dejamos el tercer brazo como extensión)
function updateIK() {
  const dx = targetPos.x;
  const dy = targetPos.y;
  const dist = Math.sqrt(dx * dx + dy * dy);
  const maxReach = L1 + L2 + L3 - 0.001;
  const clampedDist = Math.min(dist, maxReach);

  const reduced = Math.max(0.001, clampedDist - L3);

  // --- IK clásico para 2 segmentos ---
  const cosA2 = (L1 * L1 + L2 * L2 - reduced * reduced) / (2 * L1 * L2);
  const a2 = Math.acos(THREE.MathUtils.clamp(cosA2, -1, 1));
  const a1 = Math.atan2(dy, dx) - Math.atan2(L2 * Math.sin(a2), L1 + L2 * Math.cos(a2));

  // --- LIMITES ANGULARES ---
  // Brazo 1: inclinación general
  const clampedA1 = THREE.MathUtils.clamp(a1, THREE.MathUtils.degToRad(-45), THREE.MathUtils.degToRad(75));

  // Brazo 2: rango reducido para evitar que se pliegue demasiado
  const clampedA2 = THREE.MathUtils.clamp(a2, THREE.MathUtils.degToRad(10), THREE.MathUtils.degToRad(110));

  // --- APLICAR ROTACIONES ---
  brazo1.rotation.z = clampedA1;
  joint.rotation.z = Math.PI - clampedA2;

  // --- BRAZO 3: se orienta suavemente hacia el target ---
  const joint2World = new THREE.Vector3();
  joint2.getWorldPosition(joint2World);

  const toTarget = new THREE.Vector3(dx, dy, 0).sub(joint2World);
  const angleToTarget = Math.atan2(toTarget.y, toTarget.x);

  // Ángulo local respecto a los anteriores
  const totalPrevAngle = brazo1.rotation.z + joint.rotation.z;
  let localA3 = angleToTarget - totalPrevAngle;

  // Limitamos su rango también
  localA3 = THREE.MathUtils.clamp(localA3, THREE.MathUtils.degToRad(-30), THREE.MathUtils.degToRad(40));

  // Aplicamos una fracción para que no se sobreajuste
  joint2.rotation.z = localA3 * 0.8;

  // --- Mover target visible ---
  target.position.set(dx, dy, 0);
}





function animate() {
  requestAnimationFrame(animate);
  // opcional: base hacia la dirección X (muy suave)
  base.rotation.y = Math.atan2(targetPos.x, 4) * 0.3;

  updateIK();
  controls.update();
  renderer.render(scene, camera);
}
animate();
