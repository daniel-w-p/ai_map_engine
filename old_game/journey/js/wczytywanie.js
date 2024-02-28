//WAŻNE
//Pasek ładowania musi zawsze mieć id = 'postep'
//to jest klasa

function Wczytywanie()
{
	//tablica na adresy obrazów do wczytania
	this.tabAdres = new Array();
	
	//adresy grafik
	tabAdres = ['back', 'belka', 'items', 'postacP', 'skokP', 'postacL', 'skokL' ,'pauza', 'panel', 'okno', 'map', 'ogien1', 'chmura', 'meteor'];
	
	this.zaladObr = 0; //wczytane grafiki
	this.ileGrafik = 14;//tabAdres.length;
	this.szerPrzesk = 100/this.ileGrafik; //szerokość o jaką przesunie się pasek
	
	this.postep = progres;
	this.obrazy = images;
	
	self = this;
}

	//tu się tworzy pasek ładowania
	function progres()
	{
		self.zaladObr++;
	
		var width = self.zaladObr * self.szerPrzesk; // szerokość paska
		
		cntx.beginPath();
		cntx.strokeStyle = "rgba(0,0,255,1)";
		cntx.lineWidth = 2;
		cntx.strokeRect(450-2,370-2,100+4,20+4);
		cntx.fillStyle = "rgba(255,0,0,1)";
		cntx.fillRect(450,370,width,20);
		cntx.closePath();
		cntx.stroke();
		
		if(self.zaladObr >= 14)
		{
			cntx.fillStyle = '#ffffff';
			cntx.textAlign = "left";
			cntx.font = 'italic 18px sans-serif';
			cntx.fillText("załadowano", 452, 389);//punkty
			setTimeout(zerowanieSceny, 2000);
		}
	}
	
	//wczytywane obrazy - też private 
	function images()
	{
		var source = 'journey/image/';
		
		back = new Image(1024,768);
		back.crossOrigin = "anonymous";
		back.src = source+tabAdres[0]+'.png'; 
		back.onload = this.postep;         //dla każdego obiektu ustawiam zdarznie onload
		
		belkaImg = new Image(60,20);
		belkaImg.crossOrigin = "anonymous";
		belkaImg.src = source+tabAdres[1]+'.png'; 
		belkaImg.onload = this.postep; 
		
		owoce = new Image(40,25);
		owoce.crossOrigin = "anonymous";
		owoce.src = source+tabAdres[2]+'.png'; 
		owoce.onload = this.postep; 
		
		playerImgP[0] = new Image(360,112);
		playerImgP[0].crossOrigin = "anonymous";
		playerImgP[0].src = source+tabAdres[3]+'.png'; 
		playerImgP[0].onload = this.postep;
		
		playerImgP[1] = new Image(1200,112);
		playerImgP[1].crossOrigin = "anonymous";
		playerImgP[1].src = source+tabAdres[4]+'.png'; 
		playerImgP[1].onload = this.postep;
		
		playerImgL[0] = new Image(360,112);
		playerImgL[0].crossOrigin = "anonymous";
		playerImgL[0].src = source+tabAdres[5]+'.png'; 
		playerImgL[0].onload = this.postep;
		
		playerImgL[1] = new Image(1200,112);
		playerImgL[1].crossOrigin = "anonymous";
		playerImgL[1].src = source+tabAdres[6]+'.png'; 
		playerImgL[1].onload = this.postep;
		
		pauza = new Image(20,20);
		pauza.crossOrigin = "anonymous";
		pauza.src = source+tabAdres[7]+'.png'; 
		pauza.onload = this.postep;
		
		panel = new Image(800,50);
		panel.crossOrigin = "anonymous";
		panel.src = source+tabAdres[8]+'.png'; 
		panel.onload = this.postep;
		
		okno = new Image(200,150);
		okno.crossOrigin = "anonymous";
		okno.src = source+tabAdres[9]+'.png'; 
		okno.onload = this.postep;
		
		mapa = new Image(800,38);
		mapa.crossOrigin = "anonymous";
		mapa.src = source+tabAdres[10]+'.png'; 
		mapa.onload = this.postep;
		
		ogienImg = new Image(360,80);
		ogienImg.crossOrigin = "anonymous";
		ogienImg.src = source+tabAdres[11]+'.png'; 
		ogienImg.onload = this.postep;
		
		chmuraImg = new Image(60,30);
		chmuraImg.crossOrigin = "anonymous";
		chmuraImg.src = source+tabAdres[12]+'.png'; 
		chmuraImg.onload = this.postep; 
		
		meteorImg = new Image(120,40);
		meteorImg.crossOrigin = "anonymous";
		meteorImg.src = source+tabAdres[13]+'.png'; 
		meteorImg.onload = this.postep;
	}
var xMinus=+20;//bo część mapy pozostaje ukryta
function wczytajMape()
{
	//tu się bawię z zamianą danych z mini mapy na ekran - przenieś do wczytania mapy - całej
	canvasData = cntxMini.getImageData(mapStart, 0, 80, 38);
 
	for(var y = 0; y < canvasData.height; y++)
	{
	for(var x = 0; x < canvasData.width; x++)
	{
		var idx = (x + y * canvasData.width) * 4;//index kolejnych pikseli
		
		if(canvasData.data[idx] == 240 && canvasData.data[idx + 1] == 160 && canvasData.data[idx + 2] == 0)//pomarańczowy ale jaśniejszy niż dla ognia
		{
			meteor[liczMeteo] = new Obiekt();
			
			meteor[liczMeteo].dX = (x-xMinus)*20;
			meteor[liczMeteo].dY = y-45; //tu y zawsze będzie 0 i cofam trochę w górę
			
			meteor[liczMeteo].nrKlatki = 0;//obraz odpowiedniego owoca
			
			liczMeteo++; //zwiększam licznik na następną gruszkę
		}
		//belki
		else if(canvasData.data[idx + 0] == 170 || canvasData.data[idx + 1] == 170 || canvasData.data[idx + 2] == 170 || canvasData.data[idx + 0] == 0 && canvasData.data[idx + 1] == 0 && canvasData.data[idx + 2] == 0)//ciemno-czerwony, ciemno-niebieski i czarny
		{
			if(canvasData.data[idx + 0] == 170)
			{
				belka[liczBelek] = new BelkaCls(belkaImg);
			
				belka[liczBelek].dX = (x-xMinus)*20;
				belka[liczBelek].dY = y*20;
				
				liczBelek++; //zwiększam licznik na następną belkę
			}
			else if(liczBelek && canvasData.data[idx + 2] == 170 && belka[liczBelek-1].dY == y*20)//dodatkowo sprawdzam czy w tym samym wierszu
			{
				belka[liczBelek-1].width = (x-xMinus)*20+20-belka[liczBelek-1].dX;//bo jeden pixel odpowiada 20 - bez +20 pokazywałby początek
				//height jest na razie stały
			}
			else if(canvasData.data[idx + 1] == 170 && liczBelek && belka[liczBelek-1].dY == y*20)//jeśli ciemno zielony to kończę 
			{
				belka[liczBelek-1].panele++;
				belka[liczBelek-1].koniec = true;
			}
			else if(liczBelek && belka[liczBelek-1].dY == y*20)
			{
				belka[liczBelek-1].panele++;
			}
		}
		//chmury
		else if(canvasData.data[idx + 1] == 255 && canvasData.data[idx] == 0 || canvasData.data[idx + 2] == 255 && canvasData.data[idx] == 0)//zielony, niebieski i jasno niebieski
		{
			if(canvasData.data[idx + 1] == 255 && canvasData.data[idx + 2] == 0)
			{
				chmura[liczChmur] = new BelkaCls(chmuraImg);
				
				//współrzędne
				chmura[liczChmur].dX = (x-xMinus)*20;
				chmura[liczChmur].dY = y*20;
				//wysokość
				chmura[liczChmur].height=30;
				
				liczChmur++; //zwiększam licznik na następną belkę
			}
			else if(liczChmur && canvasData.data[idx + 1] == 255 && canvasData.data[idx + 2] == 255 && chmura[liczChmur-1].dY == y*20)//dodatkowo sprawdzam czy w tym samym wierszu
			{
				chmura[liczChmur-1].width = (x-xMinus)*20+20-chmura[liczChmur-1].dX;//bo jeden pixel odpowiada 20 - bez +20 pokazywałby początek
				//height jest na razie stały
			}
			else if(liczChmur && canvasData.data[idx + 1] == 0 && canvasData.data[idx + 2] == 255 && chmura[liczChmur-1].dY == y*20)
			{
				chmura[liczChmur-1].panele++;
			}
		}
		else if(canvasData.data[idx + 0] == 255 && canvasData.data[idx + 1] == 0 && canvasData.data[idx + 2] == 0)//czerwony
		{
			jablko[liczJablek] = new OwoceCls;
			
			jablko[liczJablek].dX = (x-xMinus)*20;
			jablko[liczJablek].dY = y*20;
			
			jablko[liczJablek].nrKlatki = 1;//obraz odpowiedniego owoca
			
			liczJablek++; //zwiększam licznik na następne jabłko
		}
		else if(canvasData.data[idx + 0] == 255 && canvasData.data[idx + 1] == 255 && canvasData.data[idx + 2] == 0)//żółty
		{
			grusza[liczGruszy] = new OwoceCls;
			
			grusza[liczGruszy].dX = (x-xMinus)*20;
			grusza[liczGruszy].dY = y*20;
			
			grusza[liczGruszy].nrKlatki = 0;//obraz odpowiedniego owoca
			
			liczGruszy++; //zwiększam licznik na następną gruszkę
		}
		else if(canvasData.data[idx + 0] == 255 && canvasData.data[idx + 1] == 0 && canvasData.data[idx + 2] == 255)//fiolet
		{
			kropla[liczKropli] = new OwoceCls;
			
			kropla[liczKropli].dX = (x-xMinus)*20;
			kropla[liczKropli].dY = y*20;
			
			kropla[liczKropli].nrKlatki = 2;//obraz odpowiedniego owoca
			
			liczKropli++; //zwiększam licznik na następną gruszkę
		}
		//ogień
		if(canvasData.data[idx + 0] == 255 && canvasData.data[idx + 1] == 170 && canvasData.data[idx + 2] == 0)//pomarańczowy ffaa00
		{
			ogien[liczOgni] = new OgienCls;
			
			ogien[liczOgni].dX = (x-xMinus)*20;
			ogien[liczOgni].dY = y*20;
			
			liczOgni++; //zwiększam licznik na następny ogien
		}
		
	}
	}
	//koniec mini mapy
}
	

