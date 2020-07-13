class AC {

	constructor(id) {
		this.id = id;
		this.particleSystem = undefined;
		this.particleCount = undefined;
		this.particles = 0;
		this.pMaterialHot = undefined;
		this.pMaterialCold = undefined;
		this.pBase = undefined;
		this.orientation = undefined;
		this.pVelocity = 2;
	}

    toggle(){

    }

	async spawn(scene, posX, posY, posZ, scaleXYZ, rotation) {
		await AC.init;

		var thisAC = this;

		return new Promise(async function (resolve, reject) {

			// clone mesh
			thisAC.body = AC.mesh.clone();
			thisAC.body.children[1].sliosID = thisAC.id;
			thisAC.body.children.splice(0,1);



			// set in world
			thisAC.body.position.set(posX, posY, posZ);
	        thisAC.body.rotation.y = rotation * (Math.PI/180);

			//scale the drone to the right size
			thisAC.body.scale.set(scaleXYZ, scaleXYZ, scaleXYZ);

			thisAC.particleCount = 500;
			thisAC.particles = new THREE.Geometry();
			thisAC.pMaterialHot = new THREE.PointsMaterial({color: 0xFF0000, size: 2});
			thisAC.pMaterialCold = new THREE.PointsMaterial({color: 0x0000FF, size: 2});


			thisAC.orientation = -1;
			if(rotation > 180){
				thisAC.orientation = 1;
			}

			var yOffset = 20;
			for(var p=0; p< thisAC.particleCount; p++){

				var pX = posX + Math.random() * (thisAC.orientation*200) ;
				if(Math.random() > 0.5){
					var pY = (posY+yOffset) + Math.random() * 15;
				}else{
					var pY = (posY +yOffset) - Math.random() * 15;
				}
				
				var pZ = posZ + Math.random() * 70;

				var particle = new THREE.Vector3(pX,pY,pZ);
				particle.velocity = new THREE.Vector3(thisAC.orientation*thisAC.pVelocity*Math.random()+(0.1*thisAC.orientation), 0 , 0 );

				thisAC.particles.vertices.push(particle);
				


			}


			thisAC.particleSystem = new THREE.Points(thisAC.particles, thisAC.pMaterialHot);

			thisAC.particleSystem.position.x -= 100;
			thisAC.particleSystem.position.z -= 35;
			//thisAC.particleSystem.position.x = thisAC.orientation*10;
			//thisAC.particleSystem.position.z = 0;
			//thisAC.particleSystem.position.y = 0;

			thisAC.pBase = new THREE.Vector3(thisAC.particleSystem.position.x, thisAC.particleSystem.position.y, thisAC.particleSystem.position.z);


			scene.add(thisAC.body);
			scene.add(thisAC.particleSystem);

			//done => resolve
			resolve(true);
		})
	}


	updateParticles(){
		if(this.particleSystem){

			this.particleSystem.rotation._y += 0.1;

			var pCount = this.particleCount;
	
			while(pCount--){
	
				var p = this.particleSystem.geometry.vertices[pCount];
	
				if(this.orientation != 1){
					if(p.x < this.pBase.x-200){
						p.x = this.pBase.x;
						p.velocity = new THREE.Vector3(this.orientation*this.pVelocity*Math.random()+(0.1 * this.orientation), 0 , 0 );;
					}

				}else{
					if(p.x > this.pBase.x+200){
						p.x = this.pBase.x;
						p.velocity = new THREE.Vector3(this.orientation*this.pVelocity*Math.random()+(0.1*this.orientation), 0 , 0 );;
					}

				}

	
				//p.velocity.x -= Math.random() * 0.01;
	
				p.add(p.velocity);
	
			}
	
			this.particleSystem.geometry.verticesNeedUpdate = true;



		}else{
			console.log("particle system not yet initialized ...");
		}
		
	}


	on(){
		this.particleSystem.visible = true;
	}

	off(){
		this.particleSystem.visible = false;
	}

	setHeating(){
		this.particleSystem.material = this.pMaterialHot;
	}

	setCooling(){
		this.particleSystem.material = this.pMaterialCold;
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
AC.init = new Promise(function (resolve, reject) {
	loadMesh('mesh/ac/ac.gltf').then(function (bs) {
	        AC.mesh = bs;
			resolve(true);
	});
})













