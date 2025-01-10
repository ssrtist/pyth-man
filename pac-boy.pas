(*  Pac-Man  Pascal Version 2.0   *)
(*  Copyright VerySoft Inc. 1992. *)
(*  CGA Supported.                *)
(*  All rights reserved.          *)

{$m 8092,0,65536}
PROGRAM PACMAN;
USES CRT, DOS, GRAPH;
CONST path = 'c:\tp\bgi';
      samelevel = 2;
      MaxLevel = 2;
      beanNUM: ARRAY[1..MaxLevel] OF INTEGER = (261,223);
      enemynum = 4;
      speed = 5;
      MusicB:array[1..9] OF INTEGER = (1,2,3,4,1,2,3,4,1);
(*Status*)
      dead=0; follow=1; around =2; flee=3;
      up = 1; right =2; down = 3; left = 4; 
(*Directions*)
      vx :ARRAY[1..4] OF INTEGER = (0,speed,0,-speed);
      vy :ARRAY[1..4] OF INTEGER = (-speed,0,speed,0);
(*Colors using*)
      pacolor    =Yellow;
      enemycolor =253;
      beancolor  =3;
      wallcolor  =LightBlue;
      doorcolor  =4;
VAR
(*Enemy Variables*)
    enemy                    : array [0..3] of pointer;
    edir, newedir, flag      : array [1..enemynum] of integer;
    enemyX, enemyY, control  : array [1..enemynum] of integer;
    oldenemyX, oldenemyY     : array [1..enemynum] of integer;

(*Pac-Man Variables*)
    pac                      : array [1..4,1..5] of pointer;
    pdir, newpdir, oldpdir   : integer;
    PacX, PacY               : integer;
    oldpacX, oldpacY         : integer;
    life, pose, oldpose, eat : integer;

(*Global Variables*)
    count, tone, MBPtr       : integer;
    atom, unit1, pit         : integer;
    maxX, maxY, minX, minY   : integer;
    score, high              : LONGINT;
    level                    : integer;
    die, MusicOn             : boolean;

(***************************************************************************)
FUNCTION chdir(direction, by:integer):integer;
BEGIN
  chdir := direction + by;
  IF direction+by > 4 THEN chdir:=direction+by-4;
END;

FUNCTION pointisthere(x,y,color:integer):boolean;
VAR point:integer;
BEGIN
  point:=getpixel(x,y);
  pointisthere:= (point=color)
END;

FUNCTION TurnOK(x,y:INTEGER):BOOLEAN;
BEGIN
  turnOK:=(x MOD atom - atom div 2 = 0) AND (y MOD atom - atom div 2 = 0)
END;

PROCEDURE ClrBuffer;
VAR TRASHKEY:CHAR;
BEGIN
  DELAY(1000);
  WHILE KEYPRESSED DO TRASHKEY:= READKEY;
END;

PROCEDURE WaitKey;
VAR TRASHKEY:CHAR;
BEGIN
  REPEAT
    IF KEYPRESSED THEN TRASHKEY:= READKEY
  UNTIL (TRASHKEY=' ') OR (TRASHKEY=#13);
END;

(***************************************************************************)
PROCEDURE INIT;
VAR key            : char;
    driver, mode   : integer;
BEGIN
  CLRSCR;
  GOTOXY(0, 20);
  WRITELN('Does this system has a VGA or SVGA card (Y/N)?');
  REPEAT
    key:=READKEY;
    WRITE(UPCASE(key));
    GOTOXY(WHEREX-1, WHEREY);
  UNTIL (UPCASE(key)='Y') OR (UPCASE(key)='N');
  WRITELN;
  IF UPCASE(key)='Y'
     THEN BEGIN driver:=0; mode:=1; Atom:=40 END
     ELSE BEGIN
          WRITELN('Then Get ONE!!!  Step on this cheap computer!!');
          HALT(0); END;
  WRITELN;
  WRITELN('DO YOU WANT MUSIC DURING GAME (Y/N)?');
  REPEAT
    key:=READKEY;
    WRITE(UPCASE(key));
    GOTOXY(WHEREX-1, WHEREY);
  UNTIL (UPCASE(key)='Y') OR (UPCASE(key)='N');
  IF UPCASE(key) = 'Y' THEN MusicOn:=True ELSE MusicOn:=False;

  INITGRAPH(driver,mode,path);
  IF GRAPHRESULT<>grOK
     THEN BEGIN WRITELN('Graphics driver not found.'); HALT(1) END;
  unit1:=atom div 2 - 7;
  pit := atom div (speed*2); (* PointIsThere Variable *)
END;

(***************************************************************************)
PROCEDURE playmusic(Frequency, Time: Integer; ON: Boolean);
BEGIN
  IF NOT ON THEN BEGIN NOSOUND; EXIT END;
  SOUND(Frequency);
  DELAY(Time);
END;

(***************************************************************************)
PROCEDURE addscore(gain:integer);
BEGIN
  score:= score+gain;
  IF SCORE > HIGH THEN HIGH:=SCORE;
END;

PROCEDURE showscore;
VAR S, H:STRING[20];
BEGIN
  STR(score, S);
  STR(high,  H);
  CLEARDEVICE;
  SETCOLOR(YELLOW);
  SETTEXTSTYLE(1,0,4);
  S:='YOUR SCORE: '+ S;
  H:='HIGH SCORE: '+ H;
  OUTTEXTXY(50,100,H);
  OUTTEXTXY(50,150,S);
END;
(***************************************************************************)
PROCEDURE box(xl,xr,yu,yd,bcolor,acolor:INTEGER);
BEGIN
    SETFILLSTYLE(1, acolor);
    BAR(xl, yu, xr, yd);
    SETCOLOR(bcolor);
    RECTANGLE(xl, yu, xr, yd);
END;

(***************************************************************************)
PROCEDURE makeenemy;
VAR X,Y,SIZE : INTEGER;     
BEGIN
  X:= 320;
  Y:= 100;
  SETCOLOR(enemycolor);
  SETLINESTYLE(0,0,1);
  ARC(X, Y, 0, 180, unit1);
  MOVETO (X-unit1,Y);
  LINEREL(0,unit1);
  LINEREL(unit1*2 div 5,0);
  LINEREL(0,-unit1*2 div 6);
  LINEREL(unit1*2 div 5,0);
  LINEREL(0,unit1*2 div 6);
  LINEREL(unit1*2 div 5,0);
  LINEREL(0,-unit1*2 div 6);
  LINEREL(unit1*2 div 5,0);
  LINEREL(0,unit1*2 div 6);
  LINEREL(unit1*2 div 5,0);
  LINEREL(0,-unit1);
  CIRCLE(X-unit1 div 2, Y, unit1 div 3);
  CIRCLE(X+unit1 div 2, Y, unit1 div 3);
  SIZE := IMAGESIZE(X-unit1,Y-unit1,X+unit1,Y+unit1);
  GETMEM(enemy[flee], SIZE);
  GETMEM(enemy[dead], SIZE);
  GETIMAGE(X-unit1,Y-unit1,X+unit1,Y+unit1,enemy[flee]^);
  SETFILLSTYLE(6,lightgreen);
  FLOODFILL(X,Y,enemycolor);
  GETMEM(enemy[follow], SIZE);
  GETMEM(enemy[around], SIZE);
  GETIMAGE(X-unit1,Y-unit1,X+unit1,Y+unit1,enemy[follow]^);
  GETIMAGE(X-unit1,Y-unit1,X+unit1,Y+unit1,enemy[around]^);
  GETIMAGE(X-unit1,Y-unit1,X+unit1,Y+unit1,enemy[dead]^);
END;

(***************************************************************************)
PROCEDURE makepac;
VAR count   :integer;
    size    :word;
    X, Y    :integer;
    arccoord:arccoordstype;

procedure draw(angle1, angle2, dir: integer);
VAR count:INTEGER;
BEGIN
  FOR count := 1 to 5 DO
  BEGIN
    X:= X + vx[dir] * 10;
    Y:= Y + vy[dir] * 8;
    SETCOLOR(pacolor);
    ARC(X, Y, angle1-count*9, angle2+count*9, unit1);
    GETARCCOORDS(arccoord);
    WITH arccoord DO
    BEGIN
      LINE(X, Y, Xstart, Ystart);
      LINE(X, Y, Xend, Yend);
    END;
    SETFILLSTYLE(1,pacolor);
    FLOODFILL(X+(dir MOD 5-3)*5+1, Y, pacolor);
    size:=IMAGESIZE(X-unit1, Y+unit1, X+unit1, Y-unit1);
    GETMEM(pac[dir, count], size);
    GETIMAGE(X-unit1, Y+unit1, X+unit1, Y-unit1, pac[dir,count]^);
    DELAY(100);
    box(X-unit1-1,X+unit1+1,Y-unit1-1,Y+unit1+1,1,0);
  END;
END;

BEGIN
  SETLINESTYLE(0,0,1);
  X:= 200;
  Y:= 220;
  draw(135,405,1);  {pac face up      dir #1}
  draw(45,315,2);   {pac face right   dir #2}
  draw(315,585,3);  {pac face down    dir #3}
  draw(225,495,4);  {pac face left    dir #4}
END;

(***************************************************************************)
PROCEDURE background;
TYPE  LevelType = array[1..12] of string[16];
      EmptyType = ARRAY[1..20, 1..4] OF INTEGER;
CONST
  bigbean: array[1..4] of pointtype =(
           (x:5; y:5), (x:27; y:5), (x:5; y:21), (x:27; y:21));
  row : array[1..2] of LevelType = (
('0000000000000000',
'2311111311111330',
'2120111001112030',
'2232301311232320',
'2212231003320320',
'2022222132222020',
'1030110010112101',
'3200330312310221',
'2013011001121120',
'2212013131120320',
'2020110200112020',
'0111111111111110'),

('0000000000000000',
'2311111311111330',
'2122113221132030',
'2210111001110320',
'2023230112323020',
'2211222132201320',
'1223010010123201',
'3022230312322021',
'2212203021220320',
'2032011201122120',
'2301230112301230',
'0111111111111110'));

  side :Array[1..2] OF EmptyType =
                    (((1,2,1,2),(14,15,1,2),(2,3,3,4),(2,3,3,4),
                    (13,14,3,4),(4,5,3,6),(11,12,3,6),(5,6,4,6),
                    (10,11,4,6),(5,6,7,8),(10,11,7,8),(7,9,5,6),
                    (-1,-1,-1,-1),(-1,-1,-1,-1),(-1,-1,-1,-1),(-1,-1,-1,-1),
                    (-1,-1,-1,-1),(-1,-1,-1,-1),(-1,-1,-1,-1),(-1,-1,-1,-1)),
                    ((1,2,1,2),(14,15,1,2),(4,7,2,3),(9,12,2,3),
                    (3,4,4,5),(5,6,4,6),(10,11,4,6),(12,13,4,5),
                    (2,3,8,9),(3,4,6,10),(5,6,7,9),(6,7,8,9),
                    (9,10,8,9),(10,11,7,9),(12,13,6,10),(13,14,8,9),
                    (1,2,10,11),(5,6,10,11),(10,11,10,11),(7,9,5,6)));{ 14,15,10,11)));}
VAR ct,boxNo,x,y: integer;

procedure put(num:char);
BEGIN
  CASE num OF
    '0': MOVEREL(atom,0);
    '1': LINEREL(atom,0);
    '2': BEGIN MOVEREL(atom,atom); LINEREL(0, -atom) END;
    '3': BEGIN LINEREL(atom,0); LINEREL(0,atom); MOVEREL(0, -atom); END;
    ELSE
  END;
END;

procedure clear(xl, xr, xu, xd: integer);
BEGIN
  box(xl*atom, xr*atom, xu*atom, xd*atom, wallcolor, 0);
END;
 
BEGIN
  SETCOLOR(YELLOW);
  SETTEXTSTYLE(3,0,4);
  OUTTEXTXY(90,0,'SUPER PAC-BOY');
  SETLINESTYLE(0,0,1);
  Y:=atom;
  REPEAT
    Y := Y+ atom div 2;
    X := atom;
    REPEAT
      X := X+atom div 2;
      BOX(X-1,X+1,Y-1,Y+1,beancolor,0);
    UNTIL X = atom * 15 - atom div 2;
  UNTIL Y = atom * 11 - atom div 2;
  (* * * * * * * * * * * * * * * * * *)
  SETLINESTYLE(0,0,3);
  MOVETO(bigbean[4].X, bigbean[4].Y);
  FOR ct:= 1 TO 4 DO
    WITH bigbean[ct] DO
      box(X*atom div 2-2,X*atom div 2+2,Y*atom div 2-2,Y*atom div 2+2,beancolor,0);
  (* * * * * * * * * * * * * * * * * *)
  SETCOLOR(wallcolor);
  FOR Y:= 1 TO 12 DO
  BEGIN
    MOVETO(0, (Y-1)*atom);
    FOR X:= 1 TO 16 DO PUT(row[(level+1) DIV samelevel, Y, X])
  END;
  FOR BoxNo:= 1 to 20 do
  clear(side[(Level+1) DIV samelevel, BoxNo,1], side[(Level+1) DIV samelevel, BoxNo,2],
        side[(Level+1) DIV samelevel, BoxNo,3], side[(Level+1) DIV samelevel, BoxNo,4]);
  SETCOLOR(doorcolor);
  LINE(atom*7, atom*6, atom*8, atom*6);
  IF life>0 THEN FOR ct:= 1 TO life-1 DO
     PUTIMAGE(15*atom+speed, ct*atom, pac[2,1]^, XORPUT);
END;

(***************************************************************************)
PROCEDURE playpac;

procedure getkey;
VAR key:char;
    count:integer;
BEGIN
  IF keypressed THEN key:=readkey;
  IF key=#0 THEN key:=readkey;
  CASE key OF
    #72: newpdir:=up;
    #75: newpdir:=left;
    #77: newpdir:=right;
    #80: newpdir:=down;
    #83,#115: MusicOn:= NOT MusicOn;
    #27: BEGIN CLOSEGRAPH; NOSOUND; HALT(1); END;
  ELSE
  END;
END;

VAR Fcolor: integer;

BEGIN
  PUTIMAGE(oldpacX-unit1,oldpacY-unit1,pac[oldpdir,oldpose]^,xorput);
  pose:=pose * ORD(pose<5) + 1;
  PUTIMAGE(pacX-unit1,pacY-unit1,pac[pdir,pose]^,Xorput);
  oldpacX:=pacX;
  oldpacY:=pacY;
  oldpdir:=pdir;
  oldpose:=pose;
  getkey;
  IF NOT pointisthere(pacX+vx[pdir]*pit,pacY+vy[pdir]*pit,wallcolor)
    THEN
    BEGIN pacX:=pacX+vx[pdir];
          pacY:=pacY+vy[pdir];
          IF pacX>16*atom then pacX:=0;
          IF pacX<0 then pacX:=15*atom;
{beans}   IF pointisthere(pacX+vx[pdir]*(pit-1)-1, pacY+vy[pdir]*(pit-1), beancolor)
          THEN BEGIN
                 if MusicOn then sound(800);
                 eat:=eat+1;
                 addscore(100);
{Super beans}    IF pointisthere(pacX+vx[pdir]*(pit-1)-2, pacY+vy[pdir]*(pit-1),beancolor)
                    THEN FOR count:= 1 to ENEMYNUM DO IF flag[count] <> dead THEN
                    BEGIN
                      addscore(2000);
                      PUTIMAGE(oldenemyX[count]-unit1,oldenemyY[count]-unit1,enemy[flag[count]]^,XORPUT);
                      flag[count]:=flee;
                      PUTIMAGE(oldenemyX[count]-unit1,oldenemyY[count]-unit1,enemy[flag[count]]^,XORPUT);
                      control[count]:=RANDOM(6);
                    END;
                 Fcolor:=getcolor;
                 setcolor(0);
                 rectangle(pacX+vx[pdir]*(pit-1)-1, pacY+vy[pdir]*(pit-1)-1, pacX+vx[pdir]*(pit-1)+1, pacY+vy[pdir]*(pit-1)+1);
                 rectangle(pacX+vx[pdir]*(pit-1)-2, pacY+vy[pdir]*(pit-1)-2, pacX+vx[pdir]*(pit-1)+2, pacY+vy[pdir]*(pit-1)+2);
                 setcolor(Fcolor);
               END;
    END;
  IF TurnOK(pacX,pacY) AND
    NOT pointisthere(pacX+vx[newpdir]*pit,pacY+vy[newpdir]*pit,wallcolor)
    OR (newpdir=chdir(pdir,2))
    THEN pdir:=newpdir;
END;

(***************************************************************************)
PROCEDURE playenemy;
VAR num, hold : INTEGER;

procedure getnewedir(num:integer);
BEGIN
  case flag[num] of
    follow: BEGIN
            IF ABS(enemyX[num]-pacX)<= ABS(enemyY[num]-pacY)
            THEN IF (enemyY[num]<pacY)
            THEN newedir[num]:=DOWN
            ELSE newedir[num]:=UP
            ELSE IF ABS(enemyX[num]-pacX) > ABS(enemyY[num]-pacY)
            THEN IF enemyX[num] > pacX
            THEN newedir[num]:=LEFT
            ELSE newedir[num]:=RIGHT
            END;
    flee, around: newedir[num]:=CHDIR(newedir[num], RANDOM(2)*2+1)
    ELSE
  END;
  IF newedir[num]=CHDIR(edir[num],2) THEN newedir[num]:=edir[num];
END;
(* * * * * * * * * * * * * *)
BEGIN
  FOR num:=1 TO enemynum DO IF flag[num] <> dead THEN
    BEGIN
      PUTIMAGE(oldenemyX[num]-unit1,oldenemyY[num]-unit1,enemy[flag[num]]^,XORPUT);
      PUTIMAGE(enemyX[num]-unit1,enemyY[num]-unit1,enemy[flag[num]]^,XORPUT);
      oldenemyX[num] := enemyX[num];
      oldenemyY[num] := enemyY[num];
    END;
(* * * * * * * * * * * * * *)
  FOR num:=1 TO enemynum DO
  BEGIN
    IF (ABS(enemyX[num]-pacX) <= 20) AND (ABS(enemyY[num]-pacY) <=20)
       THEN IF flag[num] <> flee
              THEN die:= true
              ELSE BEGIN
                     PUTIMAGE(oldenemyX[num]-unit1,oldenemyY[num]-unit1,enemy[flag[num]]^,XORPUT);
                     control[num]:=0;
                     flag[num]:=dead;
                     enemyX[num]:= atom*9 - atom div 2;
                     enemyY[num]:= atom*6 - atom div 2;
                     oldenemyX[num]:= enemyX[num];
                     oldenemyY[num]:= enemyY[num];
                     PUTIMAGE(oldenemyX[num]-unit1,oldenemyY[num]-unit1,enemy[flag[num]]^,XORPUT);
                   END;
    IF TurnOK(enemyX[num], enemyY[num])
    THEN BEGIN
         control[num]:=SUCC(control[num]);
         case control[num] of
           10: IF flag[num] = around THEN BEGIN flag[num]:= follow; control[num]:=0 END;
           60: IF flag[num] = follow THEN BEGIN flag[num]:= around; control[num]:=0 END;
           15: IF flag[num] = flee
               THEN BEGIN
                  PUTIMAGE(oldenemyX[num]-unit1,oldenemyY[num]-unit1,enemy[flag[num]]^,XORPUT);
                  flag[num]:= follow; control[num]:=0;
                  PUTIMAGE(oldenemyX[num]-unit1,oldenemyY[num]-unit1,enemy[flag[num]]^,XORPUT);
                  END;
           20: IF flag[num] = dead   THEN BEGIN flag[num]:= follow; control[num]:=0 END;
           else
         end;
         IF (flag[num] <> dead) THEN
            BEGIN
            IF NOT pointisthere(enemyX[num]+vx[newedir[num]]*pit,enemyY[num]+vy[newedir[num]]*pit,wallcolor)
               THEN BEGIN
                    edir[num]:= newedir[num];
                    getnewedir(num);
                    enemyX[num] := enemyX[num] + vx[edir[num]];
                    enemyY[num] := enemyY[num] + vy[edir[num]];
                    IF enemyX[num]>16*atom then enemyX[num]:=0;
                    IF enemyX[num]<0 then enemyX[num]:=15*atom;
                    END
             ELSE IF NOT pointisthere(enemyX[num]+vx[edir[num]]*pit,enemyY[num]+vy[edir[num]]*pit,wallcolor)
                  THEN BEGIN
                       enemyX[num] := enemyX[num] + vx[edir[num]];
                       enemyY[num] := enemyY[num] + vy[edir[num]];
                       IF enemyX[num]>16*atom then enemyX[num]:=0;
                       IF enemyX[num]<0 then enemyX[num]:=15*atom;
                       END
                  ELSE BEGIN
                         IF (newedir[num] = edir[num])
                            THEN newedir[num]:= CHDIR(newedir[num], RANDOM(2)*2+1)
                            ELSE BEGIN
                                   edir[num]:=CHDIR(newedir[num],2);
                                   getnewedir(num);
                                 END;
                       END;
            END;
         END
    ELSE BEGIN
         enemyX[num] := enemyX[num] + vx[edir[num]];
         enemyY[num] := enemyY[num] + vy[edir[num]];
         IF enemyX[num]>16*atom then enemyX[num]:=0;
         IF enemyX[num]<0 then enemyX[num]:=15*atom;
         END;
  END;
END;

PROCEDURE ShowPic(Lvl:INTEGER);
var
  Command: string[30];
  No     : String[1];
Begin
  Str(lvl, No);
  Command := 'GIRL'+No+'.VSF';
  RestoreCrtMode;
  SwapVectors;
  Exec('SVSF.EXE', Command);
  SwapVectors;
  if DosError <> 0 then
     WriteLn('FILE NOT FOUND: SVSF.EXE');
  SetGraphMode(GetGraphMode);
End;

(***************************************************************************)
PROCEDURE Menu;
BEGIN
  CLEARDEVICE;
  SETTEXTSTYLE(4,0,4);
  OUTTEXTXY(150,  1, 'Keys Defined');
  SETTEXTSTYLE(1,0,3);
  MOVETO(10,50);
  OUTTEXTXY(10,  50, 'UP ARROW');
  OUTTEXTXY(200,  50, '---- UP');
  OUTTEXTXY(10,  80, 'DOWN ARROW');
  OUTTEXTXY(200,  80, '---- DOWN');
  OUTTEXTXY(10, 110, 'LEFT ARROW');
  OUTTEXTXY(200, 110, '---- LEFT');
  OUTTEXTXY(10, 140, 'RIGHT ARROW');
  OUTTEXTXY(200, 140, '---- RIGHT');
  OUTTEXTXY(10, 170, 'S');
  OUTTEXTXY(200, 170, '---- MUSIC');
  OUTTEXTXY(10, 200, 'ESC');
  OUTTEXTXY(200, 200, '---- QUIT');
  CLRBUFFER;
  WAITKEY;
END;

(***************************************************************************)
Procedure Title;
CONST MusicT : Array[1..30] OF INTEGER =
               (2,3,4,6,6,7,6,4,2,3,4,4,3,2,3,2,3,4,6,6,7,6,4,2,3,4,4,3,3,2);
      TimeT  : Array[1..30] OF INTEGER =
               (0,0,2,2,4,1,3,3,4,1,3,3,3,3,5,1,0,1,2,4,1,3,3,4,1,3,3,3,3,7);
VAR MTPtr : INTEGER;
Begin
  MENU;
  CLEARDEVICE;
  SETCOLOR(yellow);
  SETTEXTSTYLE(1,0,6);
  OUTTEXTXY(10,250,'SUPER PAC-BOY');
  SETTEXTSTYLE(4,0,2);
  OUTTEXTXY(450,280,'R-Rated');
  SETTEXTSTYLE(1,0,3);
  SETCOLOR(CYAN);
  OUTTEXTXY(50,320,'Version 1.0  By Ken Wang(The Xpert)');
  OUTTEXTXY(50,360,'Copyright VerySoft Corp. 1992.');
  OUTTEXTXY(50,400,'All Rights Reserved.');
  CLRBUFFER;
  MTPtr := 1;
  REPEAT
    Playmusic(MusicT[MTPtr]*100+400, TimeT[MTptr]*100+50, MusicOn);
    NOSOUND;
  MTPtr := Succ(MTPtr);
  UNTIL KEYPRESSED OR (MTPtr>30);
  NOSOUND;
End;

(***************************************************************************)
PROCEDURE coping;
VAR outX, outY, ct:integer;
    Over:Boolean;

PROCEDURE Dying;
VAR ct:integer;
BEGIN
  IF life>0 THEN putimage(15*atom+speed, life*atom, pac[2,1]^, xorput);
  for ct:= 1 to 4 do
  for tone:= 2 to 11 do
      BEGIN
        putimage(pacX-unit1, pacY-unit1, pac[ct, tone DIV 2]^, XORPUT);
        IF MUSICON THEN SOUND(Tone*200); DELAY(20);
        putimage(pacX-unit1, pacY-unit1, pac[ct, tone DIV 2]^, XORPUT);
      END;
  IF MUSICON THEN SOUND(300);DELAY(100);
  NOSOUND;
END;

PROCEDURE GameOver;
VAR Inkey: Char;
BEGIN
  SETCOLOR(Yellow);
  SETTEXTSTYLE(1,0,6);
  OUTTEXTXY(outX+20, outY, 'GAME OVER');
  WaitKey;
  ShowScore;
  OUTTEXTXY(0, 400, 'CONTINUE(Y/N)? ');
  WHILE NOT (Inkey IN ['N','n','Y','y']) DO Inkey:=READKEY;
  CASE Inkey OF 'N','n': HALT(1) END;
  life:= 3;
  level:=1;
  score:=0;
  eat:=0;
  Title;
  CLEARDEVICE;
  background;
END;

BEGIN
  NOSOUND;
  Over := FALSE;
  outX := atom*4;
  outY := atom*4;
  IF die THEN
     BEGIN
       life := PRED(life);
       Over := (life=0);
       PUTIMAGE(oldpacX-unit1,oldpacY-unit1,pac[oldpdir,oldpose]^,xorput);
       FOR ct:= 1 to enemynum DO
       PUTIMAGE(oldenemyX[ct]-unit1,oldenemyY[ct]-unit1,enemy[flag[ct]]^,XORPUT);
       Dying;
     END
  ELSE BEGIN
       SETCOLOR(Yellow);
       SETTEXTSTYLE(1,0,8);
       OUTTEXTXY(outX, outY, 'You win');
       ClrBuffer;
       WaitKey;
       ShowPic(Level);
       level:=level+1;
       IF level>MaxLevel*samelevel THEN
          BEGIN
          Showscore;
          waitkey;
          CLEARDEVICE;
          SETCOLOR(LIGHTRED);
          SETTEXTSTYLE(1,0,8);
          OUTTEXTXY(150,250,'THE END.');
          ClrBuffer;
          WaitKey;
          HALT(1);
          END;
       eat:=0;
       showScore;
       CLRBUFFER;
       WAITKEY;
       CLEARDEVICE;
       background;
       END;
  IF Over THEN GameOver;
END;

(***************************************************************************)
PROCEDURE pacinit;
BEGIN
  die:=FALSE;
  MBPtr:=0;
  tone:=0;
  pacX := atom*8;
  pacY := atom*9 - atom div 2 ;
  oldpacX := pacX;
  oldpacY := pacY;
  pdir:= right; newpdir:= right; oldpdir:= right;
  oldpose:= 5; pose:= 5;
  PUTIMAGE(pacX-unit1, pacY-unit1, pac[2,5]^, XORPUT);
  DELAY(2000);
  {PUTIMAGE(pacX-unit1, pacY-unit1, pac[2,5]^, XORPUT);}
END;

(***************************************************************************)
PROCEDURE enemyinit;
BEGIN
  FOR count:= 1 to enemynum DO
    BEGIN
      enemyX[count]:= atom*9 - atom div 2;
      enemyY[count]:= atom*6 - atom div 2;
      oldenemyX[count]:= enemyX[count];
      oldenemyY[count]:= enemyY[count];
      edir[count]:= RANDOM(2)*2+2;
      newedir[count]:= down;
      flag[count] := RANDOM(2) + 1;
      control[count] := RANDOM(3)+1;
    END;
  FOR count:=1 TO enemynum DO
    PUTIMAGE(oldenemyX[count]-unit1,oldenemyY[count]-unit1,enemy[flag[count]]^,XORPUT);
END;

(***************************************************************************)
BEGIN
  INIT;
  Title;
  makeenemy;
  makepac;
  CLEARDEVICE;
  RANDOMIZE;
  MBPtr:=1;
  life:=3;
  level:=1;
  score:=0;
  high :=0;
  eat:=0;
  background;
  REPEAT
    ClrBuffer;
    pacinit;
    enemyinit;
    REPEAT
      MBPtr:=MBPtr*ORD(MBPtr<9)+1;
      Playmusic(MusicB[MBPtr]*100+400, 0, MusicOn);
      playpac;
      playenemy;
    UNTIL die OR (eat = beannum[(Level+1) DIV samelevel]);
    coping;
  UNTIL False;
END.