import { useEffect, useRef } from "react";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { PointerLockControls } from "three/examples/jsm/controls/PointerLockControls";

export default function ThreeDView() {
  const mountRef = useRef(null);

  useEffect(() => {
    const mount = mountRef.current;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      75,
      mount.clientWidth / mount.clientHeight,
      0.1,
      1000
    );

    const renderer = new THREE.WebGLRenderer({ antialias: false });
    renderer.setSize(mount.clientWidth, mount.clientHeight);
    mount.appendChild(renderer.domElement);


    // Load GLTF model
    const loader = new GLTFLoader();
    loader.load("/models/room.glb", (gltf) => {
      const model = gltf.scene;
      model.position.set(0, 0, 0); // or adjust as needed
      scene.add(model);

      // Optional: compute bounding boxes for walls/obstacles
      // model.traverse((child) => {
      //   if (child.isMesh) {
      //     child.geometry.computeBoundingBox();
      //     const box = child.geometry.boundingBox.clone();
      //     box.applyMatrix4(child.matrixWorld);
      //     wallBoxes.push(box);
      //   }
      // });

      console.log("Loaded model:", gltf);
    }, undefined, (error) => {
      console.error("❌ Error loading model:", error);
    });

    // Basic room
    // const floor = new THREE.Mesh(
    //   new THREE.PlaneGeometry(5, 10),
    //   new THREE.MeshBasicMaterial({ color: 0x222222 })
    // );
    // floor.rotation.x = -Math.PI / 2;
    // scene.add(floor);

    // const wallMaterial = new THREE.MeshBasicMaterial({ color: 0x0000ff });
    // const wall = new THREE.Mesh(new THREE.BoxGeometry(5, 3, 1), wallMaterial);
    // wall.position.set(0, 5, -25);
    // scene.add(wall);

    // Compute its bounding box
    // const wallBoxes = [];
    // wall.geometry.computeBoundingBox();
    // const wallBox = wall.geometry.boundingBox.clone();
    // wallBox.applyMatrix4(wall.matrixWorld);
    // wallBoxes.push(wallBox);

    // Camera
    camera.position.set(0, 1.6, 0); // ~eye height of a standing person

    // Lighting
    const light = new THREE.AmbientLight(0xffffff, 1);
    scene.add(light);

    const dirLight = new THREE.DirectionalLight(0xffffff, 2);
    dirLight.position.set(1, 3, 2);
    scene.add(dirLight);

    // Cube
    // const geometry = new THREE.BoxGeometry(1, 1, 1);
    // const material = new THREE.MeshStandardMaterial({ color: 0xff0000 });
    // const cube = new THREE.Mesh(geometry, material);
    // cube.position.set(0, 1, -3);
    // scene.add(cube);

    // Controls
    const controls = new PointerLockControls(camera, document.body);
    scene.add(controls.object);

    const onClick = () => {
      controls.lock();
    };
    document.addEventListener("click", onClick);

    const velocity = new THREE.Vector3();
    const direction = new THREE.Vector3();
    const keys = {};

    const onKeyDown = (event) => {
      keys[event.code] = true;
    };
    const onKeyUp = (event) => {
      keys[event.code] = false;
    };
    document.addEventListener("keydown", onKeyDown);
    document.addEventListener("keyup", onKeyUp);

    const clock = new THREE.Clock();

    // Animation loop
    function animate() {
      requestAnimationFrame(animate);

      const delta = clock.getDelta();

      if (controls.isLocked === true) {
        // Reset direction vector to avoid residue
        direction.set(0, 0, 0);

        // Set direction based on key input
        if (keys["KeyS"]) direction.z -= 1;
        if (keys["KeyW"]) direction.z += 1;
        if (keys["KeyA"]) direction.x -= 1;
        if (keys["KeyD"]) direction.x += 1;

        // Only normalize if we have movement
        if (direction.lengthSq() > 0) {
        direction.normalize();
        }
        
        // Create player bounding box for collision detection
        const playerBox = new THREE.Box3();

        // Friction
        velocity.x -= velocity.x * 10.0 * delta;
        velocity.z -= velocity.z * 10.0 * delta;

        // Acceleration
        velocity.x += direction.x * 50.0 * delta;
        velocity.z += direction.z * 50.0 * delta;

        // Apply movement
        // Calc next position
        const nextPosition = camera.position.clone();
        const moveX = velocity.x * delta;
        const moveZ = velocity.z * delta;
        nextPosition.x += moveX;
        nextPosition.z += moveZ;

        // Define player bounding box (small box around camera)
        const boxSize = 0.5; // width of the player
        playerBox.setFromCenterAndSize(nextPosition, new THREE.Vector3(boxSize, 1.6, boxSize));

        // Check collision with walls
        let blocked = false;
        // for (const wallBox of wallBoxes) {
        //   if (playerBox.intersectsBox(wallBox)) {
        //     blocked = true;
        //     break;
        //   }
        // }

        // Apply movement only if not blocked
        if (!blocked) {
          controls.moveRight(moveX);
          controls.moveForward(moveZ);
        }

        // Prevent sinking
        if (camera.position.y < 1.6) {
        camera.position.y = 1.6;
        }

        // Debug output (if needed)
        // console.log("Player position:", camera.position);
        // console.log("Next position:", nextPosition);
        // console.log("Player box:", playerBox);
        // console.log("Blocked:", blocked);

      }

      renderer.render(scene, camera);
    }
    animate();

    return () => {
      document.removeEventListener("click", onClick);
      document.removeEventListener("keydown", onKeyDown);
      document.removeEventListener("keyup", onKeyUp);
      mount.removeChild(renderer.domElement);
    };
  }, []);

  return <div ref={mountRef} style={{ width: "100vw", height: "100vh" }} />;
}
