class Plant {

	constructor(id) {
		this.id = id;
	}

	toggle() {

	}

	async spawn(scene, posX, posY, posZ, scaleXYZ, rotation) {
		await Plant.init;

		var thisPlant = this;

		return new Promise(async function (resolve, reject) {

			// clone mesh
			thisPlant.body = Plant.mesh.clone();



			// assemble group
			thisPlant.group = new THREE.Group();
			thisPlant.group.add(thisPlant.body);

			// set in world
			thisPlant.group.position.set(posX, posY, posZ);
			thisPlant.group.rotation.y = rotation * (Math.PI / 180);

			//scale the drone to the right size
			thisPlant.group.scale.set(scaleXYZ, scaleXYZ, scaleXYZ);

			// add the drone to the THREE.js scene
			scene.add(thisPlant.group);

			//done => resolve
			resolve(true);
		})
	}

	setPosition(x, y, z) { // x=horizontal axis1,  y=vertical axis = height, z=horizontal axis2
		this.getPosition().x = x;

		if (y > this.heightMin) {
			this.getPosition().y = y;
		} else {
			this.getPosition().y = this.heightMin;
		}
		this.getPosition().z = z;
	}

	getPosition() {
		return this.group.position;
	}



}

// initialize and load static meshes used for all class instances
Plant.init = new Promise(function (resolve, reject) {
	loadMesh('mesh/plant/plant.gltf').then(function (mesh) {
		Plant.mesh = mesh;
		resolve(true);
	});
})













