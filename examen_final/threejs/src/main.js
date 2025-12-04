console.log("CARGÓ mainFinal.js");
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

// RENDER
const renderer = new THREE.WebGLRenderer({ antialias:true });
renderer.setSize(window.innerWidth, window.innerHeight);
// ✨ CORRECCIÓN DE COLOR: Activa sRGB para corregir el brillo y la visualización de texturas
renderer.outputColorSpace = THREE.SRGBColorSpace; 
document.body.appendChild(renderer.domElement);

// ESCENA
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101010);

// CÁMARAS
const aspect = window.innerWidth / window.innerHeight;
const camPersp = new THREE.PerspectiveCamera(60, aspect, 0.1, 1000);
camPersp.position.set(4,3,7);

const camOrtho = new THREE.OrthographicCamera(-5*aspect,5*aspect,5,-5,0.1,100);
camOrtho.position.set(7,7,7);

let activeCam = camPersp;

// ORBIT CONTROLS
const controls = new OrbitControls(activeCam, renderer.domElement);

// LUCES (CORREGIDO)
const pointLight = new THREE.PointLight(0xffffff, 1.2);
pointLight.position.set(4, 6, 5);
scene.add(pointLight);

const directionalLight = new THREE.DirectionalLight(0x99ccff, 0.7);
directionalLight.position.set(-5, 3, -2);
scene.add(directionalLight);


// TEXTURAS
const loader = new THREE.TextureLoader();
// RUTAS CORREGIDAS
const tex_piso = loader.load("../textures/marmol.jpg");
const tex_metal = loader.load("../textures/metal.jpeg");

// CORRECCIÓN DE UV MAPPING
tex_piso.wrapS = THREE.RepeatWrapping;
tex_piso.wrapT = THREE.RepeatWrapping;
tex_piso.repeat.set(8, 8); 


// PISO
const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(15,15),
    new THREE.MeshStandardMaterial({ map: tex_piso })
);
ground.rotation.x = -Math.PI/2;
scene.add(ground);

// FIGURAS
const cube = new THREE.Mesh(
    new THREE.BoxGeometry(1,1,1),
    new THREE.MeshStandardMaterial({ map: tex_metal })
);
cube.position.set(-1,1,0);
scene.add(cube);

const sphere = new THREE.Mesh(
    new THREE.SphereGeometry(0.7,32,32),
    new THREE.MeshStandardMaterial({ color:0x55aaff })
);
sphere.position.set(2,1,0);
scene.add(sphere);

const torus = new THREE.Mesh(
    new THREE.TorusGeometry(0.7,0.25,16,100),
    new THREE.MeshStandardMaterial({ color:0xff5555 })
);
torus.position.set(0,1.5,-2);
scene.add(torus);

// ---- ANIMACIÓN ----
function animate(){
    requestAnimationFrame(animate);

    cube.rotation.y += 0.01;
    sphere.rotation.x += 0.015;
    torus.rotation.z += 0.012;

    renderer.render(scene, activeCam);
    controls.update();
}
animate();

// ---- CAMBIO DE CÁMARA ----
document.getElementById("btnCam").onclick = ()=>{
    activeCam = (activeCam===camPersp)? camOrtho : camPersp;
    controls.object = activeCam; 
    controls.update();
};

// ---- RESPONSIVE ----
window.addEventListener("resize", ()=>{
    renderer.setSize(window.innerWidth, window.innerHeight);
    
    camPersp.aspect = window.innerWidth/window.innerHeight;
    camPersp.updateProjectionMatrix();

    const asp=window.innerWidth/window.innerHeight;
    camOrtho.left=-5*asp; camOrtho.right=5*asp;
    camOrtho.updateProjectionMatrix();
});