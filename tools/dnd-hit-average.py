import random

class DungeonCharacter:
	hitMod = 0
	damMod = 0
	damageDie = [0] * 20
	brutalCritDice = 0
	lowestCrit = 20
	smite = [0] * 4
	eldritchSmiteLevel = 0
	eldritchSmiteCount = 0
	sneakDice = 0
	attackCount = 0
	autoHit = 0
	autoCrit = 0

	def roll(self, sides):
		return random.randint(1, sides)

	def roll20(self, rollType):
		ret = 0
		roll1 = self.roll(20)
		roll2 = self.roll(20)
		if (rollType > 0):
			if (roll1 >= roll2):
				ret = roll1
			else:
				ret = roll2
		elif (rollType < 0):
			if (roll1 <= roll2):
				ret = roll1
			else:
				ret = roll2
		else:
			ret = roll1
		return ret

	def rollDamage(self, previousAttacks):
		# Roll normal damage
		finalDamage = 0
		for x in range(0, len(self.damageDie)):
			for y in range(self.damageDie[x]):
				finalDamage += self.roll(x + 1)

		# Roll Sneak attack if needed
		if (previousAttacks == 0):
			for x in range(self.sneakDice):
				finalDamage += self.roll(6)

		# Roll smites if needed
		for x in range(len(self.smite) - 1, -1, -1):
			if (self.smite[x] > previousAttacks):
				if (self.smite[x] > 0):
					for y in range(x + 2):
						finalDamage += self.roll(8)
				break
			else:
				previousAttacks -= self.smite[x]

		# Eldritch Smite
		if (self.eldritchSmiteCount > previousAttacks):
			for x in range(self.eldritchSmiteLevel):
				finalDamage += self.roll(8)

		return finalDamage

	def attack(self, targetAC, rollType, previousAttacks):
		finalDamage = 0
		attackRoll = self.roll20(rollType)

		# Check if hit
		if (attackRoll + self.hitMod >= targetAC or self.autoHit > 0):
			
			# Roll normal damage dice
			finalDamage += self.rollDamage(previousAttacks)
			if (attackRoll >= self.lowestCrit or self.autoCrit > 0):

				# Roll more damage dice for crit
				finalDamage += self.rollDamage(previousAttacks)

				# Determine brutal crit die and roll
				for x in range(len(self.damageDie) - 1, -1, -1):
					if (self.damageDie[x] > 0):
						for x in range(brutalCritDice):
							finalDamage += roll(x + 1)
					break
			
			finalDamage += self.damMod
		
		return finalDamage

	def attackRound(self, targetAC, rollType):
		successfulAttacks = 0
		finalDamage = 0
		for x in range(self.attackCount):
			dam = self.attack(targetAC, rollType, successfulAttacks)
			finalDamage += dam
			if (dam > 0):
				successfulAttacks += 1
		return finalDamage

print("Target AC | Disadvan |   Normal | Advantage")
print("----------+----------+----------+----------")

player = DungeonCharacter()
player.hitMod = 12
player.damMod = 9
player.damageDie[11] = 1
player.brutalCritDice = 1
player.attackCount = 6
player.lowestCrit = 18
player.autoCrit = 0
player.sneakDice = 0

#dis = 0.0
#adv = 0.0
#nor = 0.0
#for x in range(10000):
#	dis += player.roll20(-1)
#	nor += player.roll20(0)
#	adv += player.roll20(+1)
#print("Dis, nor, adv: {}, {}, {}".format(dis, nor, adv))

for x in range(11):
	dis_dam = 0.0
	adv_dam = 0.0
	nor_dam = 0.0
	for y in range(10000):
		dis_dam += player.attackRound((x + 15), -1)
		nor_dam += player.attackRound((x + 15), 0)
		adv_dam += player.attackRound((x + 15), 1)
	dis_dam = dis_dam / 10000.0
	nor_dam = nor_dam / 10000.0
	adv_dam = adv_dam / 10000.0
	print(" {0:8d} | {1:8.2f} | {2:8.2f} | {3:8.2f}".format(x + 15, dis_dam, nor_dam, adv_dam))

input()