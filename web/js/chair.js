class Chair {

	constructor(id) {
		this.id = id;
	}

    toggle(){

    }

	async spawn(scene, posX, posY, posZ, scaleXYZ, rotation) {
		await Chair.init;

		var thisChair = this;

		return new Promise(async function (resolve, reject) {

			// clone mesh
			thisChair.body = Chair.mesh.clone();
			thisChair.body.position.set(posX,posY,posZ);
			thisChair.body.rotation.y =rotation * (Math.PI/180);
			thisChair.body.scale.set(scaleXYZ,scaleXYZ,scaleXYZ);
			thisChair.body.castShadow = true;
			thisChair.body.receiveShadow = true;
			thisChair.body.sliosID = thisChair.id;

            // blob to visualize chair is occupied
            var geometry = new THREE.SphereGeometry( 0.1, 32, 32 );
            var material = new THREE.MeshLambertMaterial( {color: 0xff0000} );
            var blob = new THREE.Mesh( geometry, material );
            blob.position.x = thisChair.body.position.x;
            blob.position.y = thisChair.body.position.y;
            blob.position.z = thisChair.body.position.z;
            blob.position.y += 55;
            blob.position.z += 0.1;
            blob.visible = false;
            blob.scale.set(scaleXYZ,scaleXYZ,scaleXYZ);
            blob.sliosID = thisChair.id+"_blob";
            thisChair.blob = blob;

			scene.add(thisChair.body);
			scene.add(thisChair.blob);

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
Chair.init = new Promise(function (resolve, reject) {
	loadMesh('mesh/chair/chair.gltf').then(function (chair) {
	        Chair.mesh = chair;
			resolve(true);
	});
})













