var currentlyPressedKeys = new Array();//tablica na klawisze

//wszystko co związane z klawiaturą
  function handleKeyDown(event)
  {
    currentlyPressedKeys[event.keyCode] = true;//wciśnięty 
  }
  function handleKeyUp(event)
  {
    currentlyPressedKeys[event.keyCode] = false;//puszczony
		player.buttonUp=true;
  }
  
  function g_klawisze()//obsługa poszczególnych klawiszy kiedy true
  {
		if (currentlyPressedKeys[32])
		{
			stopGame();
		}
		if (currentlyPressedKeys[87] && currentlyPressedKeys[68] || currentlyPressedKeys[87] && currentlyPressedKeys[65] || currentlyPressedKeys[38] && currentlyPressedKeys[37] || currentlyPressedKeys[38] && currentlyPressedKeys[39])
		{//skok w biegu
			// 'W' 
			//if(player.dY < 0) player.dY = 0;
			if(player.stoi && player.buttonUp)
			{
				player.jump = 16;
				player.onAir=true;
				player.buttonUp=false;
				dzwiekBiegu.currentTime = 0;//wyłączam bieg
			}
		}	
		else if (currentlyPressedKeys[87] || currentlyPressedKeys[38])
		{//skok w miejscu
			// 'W' 
			if(player.nrKlatki != 0 && player.buttonUp && !player.onAir) player.nrKlatki = 0;
			else if(player.stoi && player.buttonUp && !player.onAir)
			{
				player.jumpUp = 16;
				player.szerKl=100;//bo klatki skoku są szersze
				player.nrKlatki=0;//animacja
				player.onAir=true;
				player.buttonUp=false;
				
			}
		}	
		if (currentlyPressedKeys[83])
		{
			// 'S' 
			//if(player.dY >= 610) player.dY = 610;
			//else player.dY += 3;
		}		
		if (currentlyPressedKeys[65] || currentlyPressedKeys[37])
		{
			// 'A' 
			if(player.dX <= 4) player.dX = 4;
			else if(player.stoi)//kiedy stoi na podłożu może chodzić
			{
				player.dX -= player.speed;
				player.rodzAnim=2;
				player.animate();
				//dzwięk
				if(dzwiekBiegu.currentTime > 0.7)
					dzwiekBiegu.currentTime = 0;
				//if(!player.onAir)dzwiekBiegu.play();
			}
			else//a kiedy spada może odrobinę zmieniać kierunek
				player.dX -=2;
		}		
		if (currentlyPressedKeys[68] || currentlyPressedKeys[39])
		{
			// 'D'
			if(player.dX >= 600-player.width) player.dX = 600-player.width;
			else if(player.stoi)//kiedy stoi na podłożu może chodzić
			{
				player.dX += player.speed;
				player.rodzAnim=1;
				player.animate();
				//dzwięk
				if(dzwiekBiegu.currentTime > 0.7)
					dzwiekBiegu.currentTime = 0
				//if(!player.onAir)dzwiekBiegu.play();
			}
			else//a kiedy spada może odrobinę zmieniać kierunek
				player.dX +=2;
		}
		if(!currentlyPressedKeys[68] && !currentlyPressedKeys[65] &&!currentlyPressedKeys[39] && !currentlyPressedKeys[37] && !player.onAir)
		{
			player.stop();
		}
  }