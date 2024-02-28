//wszystkie animacje ruchy i obroty są tu wywoływane ale definiowane w java/NaScenie
function g_Animuj() 
{
	var idxX=0;
	var idxY=0;
	
	
	//jak koniec poziomu to
	if(player.finish)
	{
		replayGame();
	}
	
	
	//animuje meteory
	for(i=0; i<liczMeteo; i++)
	{
		meteor[i].nrKlatki+=0.25;//dzięki math.floor zwolnie animacje o połowę
		meteor[i].dX -= 10;
		meteor[i].dY += 15;
		if(meteor[i].nrKlatki>2)meteor[i].nrKlatki=0;
		//jeśli postać  włazi na ogień
		if(player.dX-45 < meteor[i].dX && player.dX+45 > meteor[i].dX && meteor[i].dY > player.dY && meteor[i].dY < player.dY+100)
		{
			player.dX -= 30;//odrzut
			player.live --;//wpływ na zycie
		}
	}
	
	//animuje ogniki
	for(i=0; i<liczOgni; i++)
	{
		ogien[i].nrKlatki+=0.5;//dzięki math.floor zwolnie animacje o połowę
		if(ogien[i].nrKlatki>5)ogien[i].nrKlatki=0;
		//jeśli postać  włazi na ogień
		if(player.dX-45 < ogien[i].dX && player.dX+45 > ogien[i].dX && ogien[i].dY > player.dY && ogien[i].dY < player.dY+100)
		{
			if(player.rodzAnim==1)
			{
				player.dX -= 30;
			}
			else if(player.rodzAnim==2)
			{
				player.dX += 30;
			}
			player.live --;
		}
	}
	
	player.stoi = false;//zakładam że nie stoi na belce
	
	
	for(i=0; i<liczJablek; i++)//sprawdzam po kolei wszystkie jabłka
	{
		if(jablko[i].find==false && player.dX-15 < jablko[i].dX && player.dX+55 > jablko[i].dX && jablko[i].dY > player.dY && jablko[i].dY < player.dY+100)//jeśli postać  włazi na jabłko
		{
			jablko[i].find=true;//znalezione nie wyświetla ani nie daje punktów   +20 to jest to przesunięcie o 400px
			canvasData.data[(Math.floor(jablko[i].dX/20+20) + Math.floor(jablko[i].dY/20) * canvasData.width) * 4+1]=255; //zmazuję dane z mapy
			canvasData.data[(Math.floor(jablko[i].dX/20+20) + Math.floor(jablko[i].dY/20) * canvasData.width) * 4+2]=255;
			//canvasData.data[(Math.floor(jablko[i].dx/20) + Math.floor(jablko[i].dY/20) * canvasData.width) * 4]=0;
			player.points++;//dodaje punkty
			//dzwięk
			dzwiekZderzen.play();
		}
	}
	
	for(i=0; i<liczKropli; i++)//sprawdzam po kolei wszystkie jabłka
	{
		if(kropla[i].find==false && player.dX-15 < kropla[i].dX && player.dX+55 > kropla[i].dX && kropla[i].dY > player.dY && kropla[i].dY < player.dY+100)//jeśli postać  włazi na jabłko
		{
			kropla[i].find=true;//znalezione nie wyświetla ani nie daje punktów   +20 to jest to przesunięcie o 400px
			canvasData.data[(Math.floor(kropla[i].dX/20+20) + Math.floor(kropla[i].dY/20) * canvasData.width) * 4+1]=255; //zmazuję dane z mapy
			player.points += 10;//dodaje punkty
			//dzwięk
			dzwiekZderzen.play();
		}
	}
	
	for(i=0; i<liczGruszy; i++)//sprawdzam po kolei wszystkie gruszki
	{
		if(grusza[i].find==false && player.dX-15 < grusza[i].dX && player.dX+55 > grusza[i].dX && grusza[i].dY > player.dY && grusza[i].dY < player.dY+100)
		{
			grusza[i].find=true;//jak wyżej
			canvasData.data[(Math.floor(grusza[i].dX/20+20) + Math.floor(grusza[i].dY/20) * canvasData.width) * 4+2]=255;
			//canvasData.data[(Math.floor(grusza[i].dX/20) + Math.floor(grusza[i].dY/20) * canvasData.width) * 4]=0;
			player.points += 5;
			//dzwięk
			dzwiekZderzen.play();
		}
	}
	
	//lądowanie na belkach
	for(i=0; i<liczBelek; i++)//sprawdzam po kolei wszystkie belki
	{
		if(player.dX + 30 > belka[i].dX && player.dX + 30 < belka[i].width+belka[i].dX && player.dY+112 > belka[i].dY && player.dY+104 < belka[i].dY)//tu to sprawdzam - czy stoi
		{
			player.stoi = true;//jeśli stoi to nie spadnie
			player.onAir = false;//czyli nie jest w powietrzu
			player.ktoraBelka=i;//na tej belce stoi
			//a tu sprawdzę czy nie stoi na ostatniej
			if(belka[i].koniec == true)
			{
				player.finish = true;
			}
			
			//dzwięk
			if(player.spada == true)//zaraz po upadku
			{
				dzwiekUpadku.play();
				player.spada = false;
			}
		}
	}
	//lądowanie na chmurach
	for(i=0; i<liczChmur; i++)//sprawdzam po kolei wszystkie chmury
	{
		if(player.dX + 30 > chmura[i].dX && player.dX + 30 < chmura[i].width+chmura[i].dX && player.dY+112 > chmura[i].dY && player.dY+104 < chmura[i].dY)//tu to sprawdzam - czy stoi
		{
			player.stoi = true;//jeśli stoi to nie spadnie
			player.onAir = false;//czyli nie jest w powietrzu
			//player.ktoraBelka=i;//na tej belce stoi
			
			//dzwięk
			if(player.spada == true)//zaraz po upadku
			{
				dzwiekUpadku.play();
				player.spada = false;
			}
		}
	}
	
	//spadanie
	if(!player.jump && !player.stoi && !player.jumpUp)//jeśli nie stoi na belce i akurat nie skacze to spada
	{
		player.dY += 7;
		player.spada = true;
	}
	
	//skok w dal
	if(player.jump > 0)//jeśli skacze
	{
		player.onAir = true;//jest w powietrzu
		
		if(player.jump < 3)player.nrKlatki=4;
		else player.nrKlatki=3;
		player.jump--;//żeby w końcu przestał lecieć
		
		if(player.jump > player.jumpMax/2-3)player.dY -= 2;//żeby przy skoku dawał trochę do góry
		else player.dY += 2;
		
		if(player.rodzAnim==1)player.dX += 5;//żeby przesuwał się w lewo albo prawo
		else if(player.rodzAnim==2)player.dX -= 5;
	}
	else player.jump=0;//po skoku 
	//skok w górę
	if(player.jumpUp > 0)//jeśli skacze
	{
		player.onAir = true;//jest w powietrzu
		
		//mam 12 klatek a animacja trwa 16 więc na początku nie animuję też dobre jak belka nad głową
		if(player.jumpUp > 12)player.nrKlatki=0;
		
		//mocny skok w górę
		player.dY -= 10;
		
		//na ostatnim poziomie nie ma co skakać w górę
		if(player.dY < 25)
		{
			player.jumpUp = 0;
			player.szerKl=60;//szerokość klatki wraca do normy
		}
		else//jak nie to sprawdzam belki
		{
			//żeby przywalił głową w belkę
			for(i=0; i<liczBelek; i++)
			{
				if(player.dX + 45 > belka[i].dX && player.dX + 15 < belka[i].width+belka[i].dX && player.dY < belka[i].dY+20 && player.dY > belka[i].dY)
				{
					player.jumpUp = 0;
					player.szerKl=60;//szerokość klatki wraca do normy
					//dzwięk
					dzwiekUpadku.play();
				}
			}
			for(i=0; i<liczChmur; i++)
			{
				if(player.dX + 45 > chmura[i].dX && player.dX + 15 < chmura[i].width+chmura[i].dX && player.dY < chmura[i].dY+20 && player.dY > chmura[i].dY)
				{
					player.jumpUp = 0;
					player.szerKl=60;//szerokość klatki wraca do normy
					//dzwięk
					dzwiekUpadku.play();
				}
			}
		}
		if(player.rodzAnim==1 && player.jumpUp<4)player.dX -= 8;//żeby przesuwał się w lewo albo prawo pod koniec lotu
		else if(player.rodzAnim==2 && player.jumpUp<4)player.dX += 8;
		
		player.nrKlatki++;
		if(player.nrKlatki > 11)
		{
			player.szerKl=60;//szerokość klatki wraca do normy
			player.nrKlatki=0;//jak skacze to odliczam do 12
		}
		
		player.jumpUp--;//żeby w końcu przestał lecieć
	}
	else 
	{
		player.jumpUp=0;//po skoku
		player.szerKl=60;//szerokość klatki wraca do normy
	}
	//jak przeleci w dół
	if(player.dY > 620) 
	{
		if(player.rodzAnim==1)
		{
			player.dX = belka[player.ktoraBelka].dX;//cofnięcie na bęlkę odpowiednio do kierunku ruchu
		}
		else if(player.rodzAnim==2)
		{
			player.dX = belka[player.ktoraBelka].dX + belka[player.ktoraBelka].width-60;//żeby było zawsze z innego końca niż spadł
		}
		player.dY = 0;
		player.live -= 3;
	}
	
	//jeśli postać przejdzie za 800px to przesuwam całą mapę o 200px w lewo a jeśli za 200...
	if((player.dX > 800 || przesunMape>0 && przesunMape<200) && mapStart <= 710)
	{
		//if(przesunMape==200)przesunMape=0;
		//przesuwam wszystko na planszy
		przesunMape += 20;
		player.dX -= 20;
		for(i=0; i<liczJablek; i++)//sprawdzam po kolei wszystkie jabłka
		{
			jablko[i].dX -= 20;
		}
	
		for(i=0; i<liczGruszy; i++)//sprawdzam po kolei wszystkie gruszki
		{
			grusza[i].dX -= 20;
		}
		
		for(i=0; i<liczKropli; i++)//sprawdzam po kolei wszystkie gruszki
		{
			kropla[i].dX -= 20;
		}
	
		for(i=0; i<liczBelek; i++)//sprawdzam po kolei wszystkie belki
		{
			belka[i].dX -= 20;
		}
		
		for(i=0; i<liczChmur; i++)//sprawdzam po kolei wszystkie belki
		{
			chmura[i].dX -= 20;
		}
		
		for(i=0; i<liczOgni; i++)//sprawdzam po kolei wszystkie ognie
		{
			ogien[i].dX -= 20;
		}
		
		for(i=0; i<liczMeteo; i++)//sprawdzam po kolei wszystkie meteory
		{
			meteor[i].dX -= 20;
		}
		
		//zakończenie przesuwania
		if(przesunMape >= 200)
		{
			cntxMini.putImageData(canvasData, mapStart, 0);//przed wczytaniem mapy muszę zaznaczyć zmiany jakie nastąpiły
			przesunMape = 0;
			mapStart += 10;
			liczBelek=0;
			liczChmur=0;
			liczKropli=0;
			liczJablek=0;
			liczGruszy=0;
			wczytajMape();
			//tło musi się w tym momencie zastąpić bo inaczej fragmenty wrócą na swoje stare miejsce
			NumerKlatki[0]=NumerKlatki[1];
			NumerKlatki[1]=NumerKlatki[2];
			NumerKlatki[2]=NumerKlatki[3];
			NumerKlatki[3]=NumerKlatki[4];
			NumerKlatki[4]=NumerKlatki[5];
			NumerKlatki[5]=NumerKlatki[6];
			NumerKlatki[6]=Math.floor(Math.random()*4); 
			
			//zapamiętuję że przesunąłem w prawo więc da się też w lewo
			ilePrzesuniec++;
		}
	}
	else if(ilePrzesuniec > 0 && player.dX < 200 || przesunMape<0 && przesunMape>-200)
	{
		//if(przesunMape==200)przesunMape=0;
		//przesuwam wszystko na planszy
		przesunMape -= 20;
		player.dX += 20;
		for(i=0; i<liczJablek; i++)//sprawdzam po kolei wszystkie jabłka
		{
			jablko[i].dX += 20;
		}
	
		for(i=0; i<liczGruszy; i++)//sprawdzam po kolei wszystkie gruszki
		{
			grusza[i].dX += 20;
		}
		
		for(i=0; i<liczKropli; i++)//sprawdzam po kolei wszystkie gruszki
		{
			kropla[i].dX += 20;
		}
	
		for(i=0; i<liczBelek; i++)//sprawdzam po kolei wszystkie belki
		{
			belka[i].dX += 20;
		}
		
		for(i=0; i<liczChmur; i++)//sprawdzam po kolei wszystkie chmury
		{
			chmura[i].dX += 20;
		}
		
		for(i=0; i<liczOgni; i++)//sprawdzam po kolei wszystkie ognie
		{
			ogien[i].dX += 20;
		}
		
		for(i=0; i<liczMeteo; i++)//sprawdzam po kolei wszystkie meteory
		{
			meteor[i].dX += 20;
		}
		
		//zakończenie przesuwania
		if(przesunMape <= -200)
		{
			cntxMini.putImageData(canvasData, mapStart, 0);//przed wczytaniem mapy muszę zaznaczyć zmiany jakie nastąpiły
			przesunMape = 0;
			mapStart -= 10;
			liczBelek=0;
			liczChmur=0;
			liczKropli=0;
			liczJablek=0;
			liczGruszy=0;
			wczytajMape();
			//tło musi się w tym momencie zastąpić bo inaczej fragmenty wrócą na swoje stare miejsce
			NumerKlatki[5]=NumerKlatki[4];
			NumerKlatki[4]=NumerKlatki[3];
			NumerKlatki[3]=NumerKlatki[2];
			NumerKlatki[2]=NumerKlatki[1];
			NumerKlatki[1]=NumerKlatki[0];
			NumerKlatki[0]=Math.floor(Math.random()*4);
			
			//zapamiętuję że przesunąłem w prawo więc da się też w lewo
			ilePrzesuniec--;
		}
	}
}

