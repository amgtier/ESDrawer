def ptInRange(ptx, pty, x1, y1, x2, y2):
	if x1 > x2:
		x1, x2 = x2, x1
	if y1 > y2:
		y1, y2 = y2, y1
	return x1 <= ptx <= x2 and  y1 <= pty <= y2

def latToCoor(lat, bl1, bl2, by1, by2):
	if bl1[0] == bl2[0]:
		lat = toMilliSec(lat)
		bl1 = toMilliSec(bl1)
		bl2 = toMilliSec(bl2)
		if bl1 > bl2:
			bl1, bl2 = bl2, bl1
		if by1 < by2:
			by1, by2 = by2, by1
		ans = (lat - bl1) * ((by2 - by1) / (bl2 - bl1)) + by1
	return ans

def longToCoor(longi, bl1, bl2, bx1, bx2):
	if bl1[0] == bl2[0]:
		longi = toMilliSec(longi)
		bl1 = toMilliSec(bl1)
		bl2 = toMilliSec(bl2)
		if bl1 > bl2:
			bl1, bl2 = bl2, bl1
		if bx1 > bx2:
			bx1, bx2 = bx2, bx1
		ans = (longi - bl1) * ((bx2 - bx1) / (bl2 - bl1)) + bx1
	return ans

def coorToLat(coor, bl1, bl2, bx1, bx2, d):
	bl1 = toMilliSec(bl1)
	bl2 = toMilliSec(bl2)
	if bl1 > bl2:
		bl1, bl2 = bl2, bl1
	if bx1 < bx2:
		bx1, bx2 = bx2, bx1
	ans = (coor - bx1) * ((bl2 - bl1) / (bx2 - bx1)) + bl1
	return toDeg(ans, d)

def coorToLong(coor, bl1, bl2, bx1, bx2, d):
	bl1 = toMilliSec(bl1)
	bl2 = toMilliSec(bl2)
	if bl1 > bl2:
		bl1, bl2 = bl2, bl1
	if bx1 > bx2:
		bx1, bx2 = bx2, bx1
	ans = (coor - bx1) * ((bl2 - bl1) / (bx2 - bx1)) + bl1
	return toDeg(ans, d)

def toMilliSec(val):
	if val[0].upper() in "NSWE":
		val = val[1:]
	val = val.split(".")
	assert len(val) == 4
	ans = 0
	for i in range(4):
		ans += int(val[i]) * 60 ** (3 - i)
	return ans

def toDeg(milli, d):
	struct = [0] * 4
	struct[0] = int(milli // 60 ** 3)
	milli %= 60 ** 3
	struct[1] = int(milli // 60 ** 2)
	milli %= 60 ** 2
	struct[2] = int(milli // 60 ** 1)
	milli %= 60 ** 1
	struct[3] = int(milli)
	return f"{d.upper()}{struct[0]:03}.{struct[1]:02}.{struct[2]:02}.{struct[3]:03}"