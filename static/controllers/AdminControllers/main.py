import math

rng = 10
dokladnosc = 0.05
scalowalnosc = 4
rozmiar = tuple([-1*rng, rng])


def createSquare1(sqr1: list, sqr2: list):
   String = ""
   dlug = 0
   iterator1 =sqr1.__iter__()
   iterator2 =sqr2.__iter__()
   for x in sqr2:
       ll = " ".join([symbol for symbol in iterator1.__next__()])
       lr = " ".join([symbol for symbol in iterator2.__next__()])
       linia = ll + " " + lr + "\n"
       dlug = (len(linia))
       String = String + linia
   return String, dlug


def mytext():
    cos = "Безмежно люблю тебе Надійко! Може я не можу обіймати тебе зараз, може я не можу тримати тебе за руку зараз, може я навіть не хлопець, котрий є фізично, лтшень уявний друг за комунікаційною стіною... Я не можу тримати тебе за руку зарнку, я не можу цілувати тебе наніч. Мені соромно, що часами я не можу зробити те, що й справді надихає чи тішить. Хоча програмісти знають математику, та нажаль мало хто уміє її розуміти... я не скажу що я її розумію всю, та є речі котрі можна передати навіть нею. Те на що ти дивишся, - це математичні принципи матричного числення, та лімітованого рівнняння кола. Зі всіх твоїх хлопців-залицяльників-шанувальників, я напевно найдивдиніший... і я буду безрозмірно щасливий, якщо ти даси мені показати тоіб цей чарівний світ стенографії, криптографії, трансляції, даних... Це найдивніша відкритка-подарунок, котру тобі дарували, вона не така красива як надруковані на папері відповідники. Але вона набагато складніша) Кохаю тебе моє сонечко. Ти моє щастя. Ти моє золотко. Ти моє дороге сонечко. Моя красуня. ............................................................................................................................................................................"
    start = 0
    while start != len(cos)-1:
        yield cos[start]
        start += 1


def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step


def render():
   y = [math.pi*math.cos(x)*scalowalnosc for x in drange(*rozmiar, dokladnosc)]
   x = [math.pi*math.sin(f)*scalowalnosc for f in drange(*rozmiar, dokladnosc)]
   value = round(min(y)*-1)*2
   my = list(map(lambda f: f + min(y)*-1 , y))
   mx = list(map(lambda f: f + min(x)*-1 , x))
   xy = list(zip(my, mx))

   dictionry ={}
   uptDick =lambda txy: dictionry.update({txy : []})
   round_xy = list(map(lambda txy: tuple((round(txy[0]), round(txy[1]))), xy))

   for tx, ty in round_xy:
       uptDick(round(tx))
   for tx, ty in round_xy:
       dictionry[tx].append(ty)
   for x_value, x_dict in dictionry.items():
       mi= min(dictionry[x_value])
       ma= max(dictionry[x_value])
       dictionry[x_value] = tuple([mi, ma])
   t = mytext()
   # odne kilce
   offset = 4
   d, z = list(), list()
   for tx in range(int(value-(value/2)+3)):
       d.append([(t.__next__() if dictionry[tx][0] < ty and dictionry[tx][1] > ty else " ") for ty in range(value)[0:value-offset]])
       z.append([(t.__next__() if dictionry[tx][0] < ty and dictionry[tx][1] > ty else " ") for ty in range(value)[offset:value]])
   polowa = len(d)
   iterator = d.__iter__()
   dupa, dlugosc = createSquare1(d, z)
   def createrectangle(lenght):
       String = ""
       for x in range(int(lenght / 2 - 1))[0::2]:
           String = String + "".join([" " for z in range(x + 1)]) + " ".join(
               [t.__next__() for z in range(int(lenght / 2 - 1) - x)]) + "\n"
       return String
   String = "<header><link href=\"https://fonts.googleapis.com/css?family=Nova+Mono\" rel=\"stylesheet\"></header><body><pre style=\"font-family: 'Nova Mono', monospace;\">"
   String = String + dupa + createrectangle(dlugosc - 2) + "<br> Dla N.</pre></body>"
   return String




