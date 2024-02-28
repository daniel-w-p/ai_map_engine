$(document).ready(
function()
{
		scenaStart(false);
});


function g_rysujScene() 
{
	cntx.clearRect(0, 0, canvasWidth, canvasHeight);// czyszczenie okna
	
	cntx.drawImage(back, NumerKlatki[0]*200, 0, 200, 768, -200-przesunMape, 0, 200, 768);//tlo
	cntx.drawImage(back, NumerKlatki[1]*200, 0, 200, 768, 0-przesunMape, 0, 200, 768);//tlo
	cntx.drawImage(back, NumerKlatki[2]*200, 0, 200, 768, 200-przesunMape, 0, 200, 768);//tlo
	cntx.drawImage(back, NumerKlatki[3]*200, 0, 200, 768, 400-przesunMape, 0, 200, 768);//tlo
	cntx.drawImage(back, NumerKlatki[4]*200, 0, 200, 768, 600-przesunMape, 0, 200, 768);//tlo
	cntx.drawImage(back, NumerKlatki[5]*200, 0, 200, 768, 800-przesunMape, 0, 200, 768);//tlo
	cntx.drawImage(back, NumerKlatki[6]*200, 0, 200, 768, 1000-przesunMape, 0, 200, 768);//tlo
	
	//wszystko co w grze się rusza
	//cntx.fillText(player.test, 100, 314);
	//cntx.fillText(player.nrKlatki, 100, 414);
	
	for(i=0; i<liczJablek; i++)
	{
		if(jablko[i].dX > -200 && jablko[i].dX < 1200 && jablko[i].find == false)jablko[i].draw();
	}
	for(i=0; i<liczKropli; i++)
	{
		if(kropla[i].dX > -200 && kropla[i].dX < 1200 && kropla[i].find == false)kropla[i].draw();
	}
	for(i=0; i<liczBelek; i++)
	{
		if(belka[i].dX > -400 && belka[i].dX < 1400)belka[i].draw();
	}
	for(i=0; i<liczChmur; i++)
	{
		if(chmura[i].dX > -400 && chmura[i].dX < 1400)chmura[i].draw();
	}
	for(i=0; i<liczGruszy; i++)
	{
		if(grusza[i].dX > -200 && grusza[i].dX < 1200 && grusza[i].find == false)grusza[i].draw();
	}
	for(i=0; i<liczOgni; i++)
	{
		if(ogien[i].dX > -400 && ogien[i].dX < 1400)ogien[i].draw();
	}
	for(i=0; i<liczMeteo; i++)
	{
		if(meteor[i].dX > -400 && meteor[i].dX < 1400)meteor[i].draw();
	}

	
	player.draw();
	
	
	cntx.drawImage(panel, 0, 0);//panel na wyniki
	//wyniki
	cntx.fillStyle = '#ddbb00';
	cntx.textAlign = "center";
	cntx.font = 'bold 14px sans-serif';
	
	cntx.fillText("PUNKTY:", 100, 14);//punkty
	cntx.fillText("ŻYCIE:", 300, 14);//życie
	cntx.fillText("POZIOM:", 500, 14);//poziom
	cntx.fillText("MAPA:", 700, 14);//plansza
	
	
	cntx.fillStyle = '#774444';
	cntx.textAlign = "center";
	cntx.font = 'italic 20px sans-serif';
	
	cntx.fillText(player.points, 100, 35);//punkty
	cntx.fillText(player.live, 300, 35);//życie
	cntx.fillText(player.level, 500, 35);//poziom
	cntx.fillText("1", 700, 35);//plansza
	
	//if(player.live <= 0)
		//game over na canvasie
		//cntx.drawImage(okno, 300, 220);
}

//myszka i fullscreen 
function toggleFullScreen() {
  if (!canvas.fullscreenElement &&    // alternative standard method
      !canvas.mozFullScreenElement && !canvas.webkitFullscreenElement) 
	{  // current working methods
    if (canvas.requestFullscreen) {
      canvas.requestFullscreen();
    } else if (canvas.mozRequestFullScreen) {
      canvas.mozRequestFullScreen();
    } else if (canvas.webkitRequestFullscreen) {
      canvas.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
    }
  } 
	else 
	{
    if (canvas.cancelFullScreen) {
      canvas.cancelFullScreen();
    } else if (canvas.mozCancelFullScreen) {
      canvas.mozCancelFullScreen();
    } else if (canvas.webkitCancelFullScreen) {
      canvas.webkitCancelFullScreen();
    }
  }
}

const minelo_max=40; //maksymalny czas jaki może minąć zamias 16 wtedy fps = 25
//funkcja odmierzająca czas
function g_skokCzasu()
{
	var czasTeraz = (new Date).getTime();
	if (ostatniRaz != 0)
	{
		minelo = czasTeraz - ostatniRaz;
		if(minelo > minelo_max)
		{
			minelo = minelo_max;//jeśli minie więcej czasu (jakiś lag) to cała scena się zatrzyma
		}
		minelo_s=minelo/1000;
	}
   ostatniRaz = czasTeraz;
}

//zerowanie obiektów, czyszczenie okna i rysowanie pierwszej klatki
	function zerowanieSceny()
	{
		player = new Postac;//player
		
		//zerowanie liczników obiektów w grze
		liczJablek=0;//liczniki dla obiektów 
		liczBelek=0;
		liczGruszy=0;
		liczChmur=0;
		liczKropli=0;
		liczOgni=0;
		ilePrzesuniec=0;
		
		cntx.clearRect(0, 0, canvasWidth, canvasHeight);// czyszczenie okna
		
		//to jest we wczytywanie.js
		cntxMini.drawImage(mapa,0,0);//wstawiam minimape do minicanvasa
		wczytajMape();//a potem resztę
		
		//jedna klatka sceny
		g_rysujScene();	//rysuje scenę w każdej klatce    rysuj.js
		//i info: naciśnij żeby zacząć
		cntx.drawImage(okno, 400, 290);
		cntx.fillStyle = '#774444';
		cntx.textAlign = "center";
		cntx.font = 'italic 20px sans-serif';
		cntx.fillText("Naciśnij,", 500, 354);//
		cntx.fillText("aby rozpocząć!", 500, 384);//
	}
	
//funkcje odpowiedzialne za animacje
	function playGame()
	{
		//opóźnienie ok 60Hz
    if(player.live!=0&&!play)
		{
			play = setInterval(animator, 40);
			playerAnim = setInterval(playator, 60);
		}
		else if(player.live==0)
		{
			zerowanieSceny();
			//opóźnienie ok 60Hz
			play = setInterval(animator, 40);
			playerAnim = setInterval(playator, 60);
		}
		flagaSpacji=true;//do pauzowania
		dzwiekGry.play();//gra muzyczka
	}
	
	function stopGame()
	{
		clearInterval(play);
		play=0;
		clearInterval(playerAnim);
		playerAnim=0;
		
		//flaga do pauzowania
		flagaSpacji=false;
		//pauza
		cntx.drawImage(pauza, 500, 380);
		dzwiekGry.pause();//nie gra
	}
	
	function replayGame()
	{
		//przerwanie odtwarzani
		clearInterval(play);
		play=0;
		clearInterval(playerAnim);
		playerAnim=0;
		
		//zeruję przesunięcie na minimapie
		mapStart=0;
		
		//flaga do pauzowania
		flagaSpacji=false;
		
		//zerowanie
		zerowanieSceny();
	}
	function switcher()
	{
		//kliknięcie pauzuje i startuje
			if(flagaSpacji==false)
			{
				playGame();
			}
			else
			{
				stopGame();
			}
	}
	//i za sterownie dźwiękiem
	function audioMute()
	{
		if(mute=!mute)
		{
			dzwiekGry.volume=0;
			dzwiekZderzen.volume=0;
		}
		else
		{
			dzwiekGry.volume=0.1;
			dzwiekZderzen.volume=0.5;
		}
	}
	
	//sprawdzam wynik i jeśli wyższy niż zapisany to zamieniam
	function spradzWynik(wynik)
	{
		if(wynik>localStorage.wynik)localStorage.wynik=wynik;
	}
	
//funkcja obsługująca całą animację sceny, czas itd
function animator()
{
	g_skokCzasu(); 	//czas od ostatniej klatki
	g_Animuj();			//obliczanie związane z ruchem			animacje.js
	g_rysujScene();	//rysuje scenę w każdej klatce    rysuj.js
}
function playator()
{
	g_klawisze()	//obsługa klawiatury
}
	
//startuje cały proces rysowania w canvas
  function scenaStart(user)
	{
		//podpinam się pod canvas
		canvas = document.getElementById("canvas1");
		cntx = canvas.getContext("2d");
		//i mały
		canvasMini = document.getElementById("miniMap");
		cntxMini = canvasMini.getContext("2d");
		
		//login gościa
		if(user) sessionStorage.user=user;
		
		//na początek sprawdzam czy ma już najlepszy wynik
		if(!localStorage.wynik)localStorage.wynik=0;
		/////////////////////////////////tworzę obiekty

		//obiekt odpowiedzialny za obsługę myszy
		//var mysz = new mycha; 

		
		//ładowanie obrazów
		LoadImages = new Wczytywanie;
		LoadImages.obrazy();
		//panel boczny
		
		//dzwięki 
		dzwiekZderzen = document.getElementById('dzwiekZderzen');
		dzwiekUpadku = document.getElementById('dzwiekUpadku');
		dzwiekBiegu = document.getElementById('dzwiekBiegu');
		dzwiekGry = document.getElementById('dzwiekGry');
		
		//////////
		
		if(!mute)
		{
			dzwiekZderzen.volume=0.7;
			dzwiekGry.volume=0.2;// to jest do muzyczki w grze
		}
													
		
		//zerowanieSceny();// zastąpione przez progres we wczytywanie.js
		
		//obsługa zdarzeń klawiatury
		document.onkeydown = handleKeyDown;
		document.onkeyup = handleKeyUp;
		
		document.onselectstart = function(){return false;};
		canvas.onclick = switcher;
		//canvas.onmousedown = mysz.handleMouseD;
		//document.onmouseup = mysz.handleMouseU;
		//document.onmousemove = mysz.handleMouseM;
		
		//zdarzenia dla przycisków start, stop itd
		var startButton=document.getElementById("start");
		var restartButton=document.getElementById("restart");
		var stopButton=document.getElementById("stop");
		var fullButton=document.getElementById("fullS");
		var soundButton=document.getElementById("sound");
		var bestButton=document.getElementById("showBest");
		startButton.addEventListener("click", playGame, false);
		restartButton.addEventListener("click", replayGame, false);
		stopButton.addEventListener("click", stopGame, false);
		fullButton.addEventListener("click", toggleFullScreen, false);
		soundButton.addEventListener("click", audioMute, false);
		//bestButton.addEventListener("click", skryptPHPload, false);
		//ten jest tylko dla zalogowanych
		var zapiszButton;
		if(zapiszButton=document.getElementById("zapiszWynik"))
			zapiszButton.addEventListener("click", skryptPHPsave, false);
		
		
		//to się przyda w razie potrzeby obrazowania dzwięku
		//var source = context.createMediaElementSource(dzwiekGry);
		//source.connect(analyser);
		//analyser.connect(context.destination);
  }

