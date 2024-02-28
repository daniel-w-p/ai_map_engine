/////// 	ZMIENNE GLOBALNE
var LoadImages = null//ładowanie grafik
var keyBoard=null;
var canvasWidth=1024; 
var canvasHeight=768;
var canvas=null;
var cntx=null; //context do canvas
var canvasMini=null;//dla mini-mapy
var cntxMini=null; //context do canvas-mini
var canvasData=null;//to jest na dane z określonego obszaru minimapy
var play=null; //interwał gry
var playerAnim=null; //interwał animacji postaci
var interwal=0;//interwał facebook
var flagaSpacji=false;//żeby spacja włączała i wyłączała gre - przerzucone na myszkę

//obiekty w grze
var player=null;
var playerImgP=new Array();
var playerImgL=new Array();
var jablko = new Array();//obiekty
var grusza = new Array();//obiekty
var kropla = new Array();//obiekty
var owoce = null;//obraz
var ogien = new Array();//muszę mieć jakieś przeszkody
var ogienImg = null;
var meteor = new Array();
var meteorImg = null;
var back = null;//tło
var belka = new Array();//belki po których biega
var belkaImg = null;
var chmura = new Array();//belki po których biega
var chmuraImg = null;
var panel=null;
var pauza=null;
var okno=null;
var mapa=null;//mini mapa

var animPlayer=false;//
var NumerKlatki=[0,1,2,3,2,1,0];//klatki tła
var mapStart=0;//to jest początek fragmentu minimapy
var przesunMape=0;//to jest miernik przesunięcia całej planszy
var ilePrzesuniec=0;//muszę to mieć żeby wiedzieć czy mogę iść w lewo
var liczJablek=0;//liczniki dla obiektów 
var liczBelek=0;//
var liczChmur=0;//
var liczGruszy=0;
var liczKropli=0;
var liczOgni=0;
var liczMeteo=0;

var testowa=0;

//zmienne czasu 
var ostatniRaz = 0;
var minelo=0;
var minelo_s=0;

//dla dżwięku
var dzwiekZderzen=null;
var dzwiekGry=null;
var dzwiekUpadku=null;
var dzwiekBiegu=null;
//var context = new webkitAudioContext();
//var analyser = context.createAnalyser();
var mute = false;


//var gameOver=null;
