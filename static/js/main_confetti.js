(function(){

  window.requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame;

  var canvas = document.querySelector("canvas");
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight;


  var ctx = canvas.getContext("2d");
  ctx.globalCompositeOperation = "source-over"; //合成方法

  //stats.js
  var stats = new Stats();
  document.body.appendChild( stats.dom );

  var particles = [];
  var pIndex = 0;
  var x, y, frameId;

  //Particle作成
  function Particle(x,vx,vy,color,size){
    this.x = x;
    this.y = -canvas.height/2;
    this.vx = vx;
    this.vy = vy;
    this.color = color;
    particles[pIndex] = this;
    this.id = pIndex;
    pIndex++;
    this.life = 0;
    this.maxlife = 600;
    this.degree = getRandom(0,360);//開始角度をずらす
    this.size = Math.floor(getRandom(size*0.8,size));//紙吹雪のサイズに変化をつける
  };

  Particle.prototype.draw = function(){
    this.degree += 1;
    this.vx *= 0.99;//重力
    this.vy *= 0.999;//重力
    this.x += this.vx+Math.cos(this.degree*Math.PI/180);//蛇行
    this.y += this.vy;
    this.width = this.size;
    this.height = Math.cos(this.degree*Math.PI/45)*this.size;//高さを変化させて、回転させてるっぽくみせる
    //紙吹雪の描写
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.moveTo(this.x+this.x/2, this.y+this.y/2);
    ctx.lineTo(this.x+this.x/2+this.width/2, this.y+this.y/2+this.height);
    ctx.lineTo(this.x+this.x/2+this.width+this.width/2, this.y+this.y/2+this.height);
    ctx.lineTo(this.x+this.x/2+this.width, this.y+this.y/2);
    ctx.closePath();
    ctx.fill();
    this.life++;
    //lifeがなくなったら紙吹雪を削除
    if(this.life >= this.maxlife){
      delete particles[this.id];
    }
  }


  //GUI
  var params,params_A,params_B,params_C;
  function setGUI(){
    params = {
      'colorful_mode': true,
      'amount': 5,
      'bg_color' : "#222",
      'vx' : 2,
      'vy' : 4,
      'size' : 10
    };

    params_A = {
      'color': "#ED1A3D",
    };

    params_B = {
      'color': "#ffd400",
    };

    var gui = new dat.GUI();
    gui.add( params, 'colorful_mode');
    gui.add( params, 'amount', 1.0, 10 ).step( 1 );
    gui.addColor( params, 'bg_color');
    gui.add( params, 'vx', 1.0, 10 ).step( 0.1 );
    gui.add( params, 'vy', 1.0, 10 ).step( 0.1 );
    gui.add( params, 'size', 5, 30 ).step( 1 );

    var fA = gui.addFolder('particle_A')
    fA.addColor( params_A, 'color');

    var fB = gui.addFolder('particle_B')
    fB.addColor( params_B, 'color');
  }
  setGUI();

  //アニメーション
  function loop(){
    ctx.clearRect(0,0, canvas.width, canvas.height); //画面の更新
    canvas.style.background = 'transparent'; //背景色変更

    if(frameId % (11-params.amount) == 0){
      //カラフルモードがONの時色がカラフルになる
      var hue = Math.floor(getRandom(0,12.99))*30;
      var hsl_color = "hsl(" + hue + ", 80%, 60%)";
      new Particle(canvas.width*Math.random(), getRandom(-params.vx, params.vx), getRandom(params.vy-2, params.vy),hsl_color,params.size);
    }

    for(var i in particles){
      particles[i].draw();
    }
    frameId = requestAnimationFrame(loop);
    if(frameId % 2 == 0) { return; }//60fpsを30fpsにする
    stats.update();
  }
  loop();

  //全画面リサイズ
  window.addEventListener("resize", function(){
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    x = canvas.width / 2;
    y = canvas.height / 2;
  });

  function getRandom(min, max) {
    return Math.random() * (max - min) + min;
  }

})();