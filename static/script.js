const canvas = document.getElementById('liquid-engine');
const ctx = canvas.getContext('2d');

let width, height;
let particles = [];



// CONFIG
const conf = {
    colorHero: 0x8A2BE2, // Purple
    colorThemes: 0x00E5FF, // Blue
    colorDev: 0xFF5E00, // Orange
    colorDownload: 0x00FF6A // Green
};

// THREE JS SETUP
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x000000, 0.04);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
camera.position.z = 5;
camera.position.y = -2;
camera.rotation.x = 0.5;

const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
container.appendChild(renderer.domElement);

// GEOMETRY
const geo = new THREE.PlaneGeometry(60, 60, 50, 50);
const mat = new THREE.MeshBasicMaterial({ 
    color: conf.colorHero, 
    wireframe: true,
    transparent: true,
    opacity: 0.3
});
const plane = new THREE.Mesh(geo, mat);
scene.add(plane);

// NOISE
const simplex = new SimplexNoise();
const posAttribute = geo.attributes.position;
let time = 0;

function animate() {
    requestAnimationFrame(animate);
    time += 0.003;

    for(let i=0; i < posAttribute.count; i++){
        const x = posAttribute.getX(i);
        const y = posAttribute.getY(i);
        const z = simplex.noise3D(x * 0.1, y * 0.1, time) * 2;
        posAttribute.setZ(i, z);
    }
    posAttribute.needsUpdate = true;
    renderer.render(scene, camera);
}
animate();

// SCROLL COLOR CHANGE
window.addEventListener('scroll', () => {
    const scroll = window.scrollY;
    const h = window.innerHeight;

    let target = new THREE.Color(conf.colorHero);

    if(scroll > h * 0.5 && scroll < h * 1.5) target.setHex(conf.colorThemes);
    else if(scroll > h * 1.5 && scroll < h * 2.5) target.setHex(conf.colorDev);
    else if(scroll > h * 2.5) target.setHex(conf.colorDownload);
    
    mat.color.lerp(target, 0.05);
});

// RESIZE
window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});

// INTERACTION
document.addEventListener('keydown', (e) => {
    let k = e.key.toUpperCase();
    if(e.code === 'Space') k = ' ';
    
    const el = document.querySelectorAll('.key');
    el.forEach(key => {
        if(key.innerText === k || (k === ' ' && key.classList.contains('space'))) {
            key.classList.add('active');
            key.style.background = '#' + mat.color.getHexString();
            key.style.boxShadow = `0 0 20px #${mat.color.getHexString()}`;
        }
    });
});

document.addEventListener('keyup', (e) => {
    const el = document.querySelectorAll('.key');
    el.forEach(key => {
        key.classList.remove('active');
        key.style.background = '#151515';
        key.style.boxShadow = 'none';
    });
});