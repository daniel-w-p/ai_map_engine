////////////////////////Klasy obiektów
//player
function Postac()
{
	this.dX=50;
	this.dY=420-8;//żebym pamiętał o wysokości tekstury
	this.live=10;//życie
	this.level=1;//poziom
	this.jump=0;//skok
	this.jumpMax=16;//skok
	this.jumpUp=0;//skok
	this.speed=6;//szybkość
	this.points=0;	//sdobyte punkty
	this.ktoraBelka=0;//na której aktualnie stoi belce
	this.rodzAnim=1;//co ma się dziać i czy w ogóle coś
	this.nrKlatki=0;//numer klatki postaci
	this.stoi=true;//żeby nie mógł się poruszać kiedy nie stoi na podłożu
	this.onAir=true;//test czy leci po skoku
	this.spada=true;//czy spada
	this.buttonUp=true;//czy puścił guzik po skoku
	this.finish=false;//koniec poziomu
	this.test=0;
	
	this.szerKl=60;//wymiary klatki
	var wysKl=112;
	
	this.stop=function()
	{
		if(this.nrKlatki!=0)
		{
			this.nrKlatki++;
			if(this.nrKlatki > 5)this.nrKlatki=0;
		}
	}
	this.animate=function()
	{
		this.nrKlatki++;
		if(this.nrKlatki > 11 && this.jumpUp>0)this.nrKlatki=0;//jak skacze to odliczam do 12
		else if(this.nrKlatki > 5)this.nrKlatki=0;//a jak nie to do 6
	}
	this.draw=function()
	{
		//rysuje postać w zależności od tego gdzie patrzy
		if(this.rodzAnim == 1)
		{//i czy skacze
			if(this.jumpUp>0)cntx.drawImage(playerImgP[1], this.nrKlatki*this.szerKl, 0, this.szerKl, wysKl, this.dX, this.dY, this.szerKl, wysKl);
			else cntx.drawImage(playerImgP[0], this.nrKlatki*this.szerKl, 0, this.szerKl, wysKl, this.dX, this.dY, this.szerKl, wysKl);
		}
		if(this.rodzAnim == 2)
		{
			if(this.jumpUp>0)cntx.drawImage(playerImgL[1], this.nrKlatki*this.szerKl, 0, this.szerKl, wysKl, this.dX, this.dY, this.szerKl, wysKl);
			else cntx.drawImage(playerImgL[0], this.nrKlatki*this.szerKl, 0, this.szerKl, wysKl, this.dX, this.dY, this.szerKl, wysKl);
		}
	}
}




//////////////////////////owoce
function Obiekt()
{
	this.dX=0;
	this.dY=0;
	this.find=false;
	this.nrKlatki=0;

	this.draw=function()
	{
		cntx.drawImage(meteorImg, Math.floor(this.nrKlatki)*40, 0, 40, 40, this.dX, this.dY, 40, 40);
	}
}

function OwoceCls()
{
	this.draw=function()
	{
		cntx.drawImage(owoce, this.nrKlatki*20, 0, 20, 25, this.dX, this.dY, 20, 25);//jabłko
	}
}

function BelkaCls(belkaImg)
{
	this.width=80;
	this.height=20;
	this.panele=1;
	this.dodaj=20;
	this.koniec=false;
	
	this.draw=function()
	{
		var i=1;//do zliczania
		cntx.drawImage(belkaImg, 0, 0, 20, this.height, this.dX, this.dY, 20, this.height);//belka
		while(i<this.panele)
		{
			cntx.drawImage(belkaImg, 20, 0, 20, this.height, this.dX+this.dodaj*i, this.dY, 20, this.height);//belka
			
			i++;
		}
		cntx.drawImage(belkaImg, 40, 0, 20, this.height, this.dX+this.width-20, this.dY, 20, this.height);//belka*/
	}
}

function OgienCls()
{
	this.nrKlatki=0;
	this.speed = 5;
	
	var szerKl=60;
	var wysKl=80;
	
	
	this.draw=function()
	{
		cntx.drawImage(ogienImg, Math.floor(this.nrKlatki)*szerKl, 0, szerKl, wysKl, this.dX, this.dY, szerKl, wysKl);
	}
}

OwoceCls.prototype = new Obiekt;
BelkaCls.prototype = new Obiekt;
OgienCls.prototype = new Obiekt;