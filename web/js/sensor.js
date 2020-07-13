class Sensor {

	constructor(id) {
		this.id = id;
	}

    toggle(){

    }

	async spawn(scene, posX, posY, posZ, scaleXYZ, rotation) {
		await Sensor.init;

		var thisSensor = this;


		return new Promise(async function (resolve, reject) {

			// clone mesh
			thisSensor.body = Sensor.mesh.clone();



			thisSensor.okMaterial = new THREE.MeshLambertMaterial({color: 0x00FF00})
			thisSensor.alarmMaterial = new THREE.MeshLambertMaterial({color: 0xFF0000})
			thisSensor.body.children[0].children[1].material = thisSensor.okMaterial;

			thisSensor.body.sliosID = thisSensor.id;
			thisSensor.body.children[0].children[0].sliosID = thisSensor.id;
			thisSensor.body.children[0].children[1].sliosID = thisSensor.id;

			// set in world
			thisSensor.body.position.set(posX, posY, posZ);
			//thisSensor.body.rotation.y = rotation * (Math.PI/180);
			//thisSensor.body.rotation.z = 90;
			//thisSensor.body.rotation.x = 270;
			thisSensor.body.rotation.x = -90 * (Math.PI/180);


			//scale the drone to the right size
			thisSensor.body.scale.set(scaleXYZ, scaleXYZ, scaleXYZ);

			// add the drone to the THREE.js scene
			scene.add(thisSensor.body);

			//done => resolve
			resolve(true);
		})
	}


	resetAlarm(){
		this.body.children[0].children[1].material = this.okMaterial;

	}

	alarm(){
		this.body.children[0].children[1].material = this.alarmMaterial;

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
Sensor.init = new Promise(function (resolve, reject) {
	loadMesh('mesh/sensor/sensor.gltf').then(function (bs) {
	        Sensor.mesh = bs;
			resolve(true);
	});
})













