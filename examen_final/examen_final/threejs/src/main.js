console.log("CARGÓ mainFinal.js y Generador de GIF");
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';


// RENDER
const renderer = new THREE.WebGLRenderer({ antialias:true });
renderer.setSize(window.innerWidth, window.innerHeight);
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

// LUCES (Corregido)
const pointLight = new THREE.PointLight(0xffffff, 1.2);
pointLight.position.set(4, 6, 5);
scene.add(pointLight);

const directionalLight = new THREE.DirectionalLight(0x99ccff, 0.7);
directionalLight.position.set(-5, 3, -2);
scene.add(directionalLight);

// TEXTURAS (Asumiendo que las rutas están corregidas o que la carpeta 'textures' está accesible)
const loader = new THREE.TextureLoader();
// Ajusta la ruta a tu entorno final: o "../textures/" o "/textures/"
const tex_piso = loader.load("../textures/marmol.jpg"); 
const tex_metal = loader.load("../textures/metal.jpg");

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


// --- LÓGICA DE GRABACIÓN DE GIF ---

// Función auxiliar para forzar la descarga
function downloadURI(uri, name) {
    const link = document.createElement('a');
    link.download = name;
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

const captureFrame = (frameNum, totalFrames, filename) => {
    // 1. Renderiza la escena
    renderer.render(scene, activeCam);

    const dataURL = renderer.domElement.toDataURL('image/png');

    
    if (frameNum === totalFrames) {
        downloadURI(dataURL, filename + '.png');
        alert("Captura de imagen de prueba '" + filename + ".png' generada. Para generar un GIF animado en el navegador, se requiere la librería gif.js.");
    }
};

let recording = false;
let frameCount = 0;
const MAX_FRAMES = 100;

document.getElementById("btnGrab").onclick = () => {
    if (recording) return;
    recording = true;
    frameCount = 0;

    
    alert("Iniciando grabación de 50 frames. Por favor, mantenga la escena visible. Se descargará una imagen PNG de prueba (simulando el final de la compilación del GIF).");
};

// --- ANIMACIÓN ---
function animate(){
    requestAnimationFrame(animate);

    cube.rotation.y += 0.01;
    sphere.rotation.x += 0.015;
    torus.rotation.z += 0.012;

    controls.update();
    
    // Lógica para la grabación de frames
    if (recording) {
        frameCount++;
        if (frameCount <= MAX_FRAMES) {
             // Simulación: Capturamos el frame y, al final, generamos una prueba.
             captureFrame(frameCount, MAX_FRAMES, "escena_prueba");
        } else {
            recording = false;
            // Después de 50 frames, la grabación se detiene
        }
    }
    
    renderer.render(scene, activeCam);
}
animate();

// --- CAMBIO DE CÁMARA (Mismo código) ---
document.getElementById("btnCam").onclick = ()=>{
    activeCam = (activeCam===camPersp)? camOrtho : camPersp;
    controls.object = activeCam; 
    controls.update();
};

// --- RESPONSIVE (Mismo código) ---
window.addEventListener("resize", ()=>{
    renderer.setSize(window.innerWidth, window.innerHeight);
    
    camPersp.aspect = window.innerWidth/window.innerHeight;
    camPersp.updateProjectionMatrix();

    const asp=window.innerWidth/window.innerHeight;
    camOrtho.left=-5*asp; camOrtho.right=5*asp;
    camOrtho.updateProjectionMatrix();
});
