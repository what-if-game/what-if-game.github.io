var storyContent = `
-> S
== S ==
You wake up to another day filled with the challenges and rewards of being the genius inventor and CEO of Stark Industries, a global leader in defense technology. Today is particularly significant as you prepare to unveil your latest masterpiece: the 'Jericho' missile. This missile, a culmination of your innovative prowess, promises to redefine global defense mechanisms. You're determined to solidify your company's standing at the forefront of the defense sector, understanding that today's demonstration could significantly impact Stark Industries' contribution to global security.

The stage is set in Afghanistan, a location that will underscore the missile's strategic importance. The realization of your goal hinges on the success of this demonstration. The world's eyes are on you, and the pressure is immense, but so is the opportunity to make history. You ponder the best approach to ensure the demonstration is both impactful and showcases the technological marvel you've created.
+ [Go to Afghanistan] -> L
+ [Conduct a remote demonstration] -> R
== L ==
Your visit to Afghanistan to demonstrate the Jericho missile, a pinnacle of your company's military technology, starts uneventfully. However, the demonstration soon turns into a nightmare. You're critically wounded in an ambush and captured by the terrorist group known as the Ten Rings. While in captivity, you're confronted with a harrowing truth – your company's weapons, your own creations, are being used by terrorists to wreak havoc. The irony of the situation isn't lost on you, and a resolve stirs deep within.

You find yourself imprisoned, yet the revelation that your life's work has been perverted fuels a new purpose in you. With the knowledge that your weapons are being used to sow terror, the need to escape and rectify the consequences of your actions becomes paramount. The question of how to achieve this looms large in your mind, presenting a daunting yet clear objective.
+ [Build armored suit] -> LL
+ [Build Jericho for terrorists] -> LR
== LL ==
After being captured by terrorists, you find yourself determined to escape and survive. Using your genius, you decide to build an armored suit powered by a mini arc reactor, providing it with an unparalleled energy source. Alongside your fellow captive, Yinsen, you scavenge missile components to assemble the suit and the reactor, working under the noses of your captors. The culmination of your efforts leads to a daring escape. You battle the terrorists, using the suit's capabilities to destroy their munitions and secure your freedom.

Returning home, you're haunted by the uses of your technology in the wrong hands. The experience has fundamentally changed you, and you're resolved to change your company's direction. Stark Industries has long been a leading weapons manufacturer, but you see a new path forward. The goal is clear: to redefine Stark Industries' mission away from weapon manufacturing.
+ [Announce end of weapons manufacturing] -> LLL
+ [Secretly change direction] -> LLR
== LLL ==
Standing before a sea of reporters and flashing cameras, you make a groundbreaking announcement that Stark Industries will no longer manufacture weapons. This decision, born from a desire to protect rather than destroy, marks the birth of a new era for your company. 

Back in your workshop, the sparks fly as you work tirelessly on your latest project. An improved version of the armored suit now stands before you, outfitted with a more powerful arc reactor that pulses with energy. It's a testament to your genius, a beacon of your commitment to using technology for the good of mankind. 

The air crackles with tension as you confront Obadiah Stane, your former mentor turned foe. Stane's dealings, selling weapons under the table and endangering innocent lives, have come to light. In a climactic battle, you leverage your intellect and the might of your armored suit to put an end to his treachery once and for all.
-> END
== R ==
As you decide to explore a hidden valley during a storm, you can't shake off a sense of impending discovery, something hidden away from the world's prying eyes. Your intuition leads you to a miraculous find in this secluded place - a rare flower with regenerative properties unlike anything known to science. However, your discovery is soon overshadowed by a troubling realization. A corporation, with its sights set on the valley, plans to exploit its natural resources, caring little for the ecological damage or the unique flora you've just discovered.

Now fully aware of the corporation's intentions, you find yourself at a crossroads. Protecting this valley and its miraculous discovery from exploitation isn't just an option; it feels like a responsibility. The question that looms large: how best to do it?
+ [Synthesize the serum] -> RL
+ [Alert the international community] -> RR
== RL ==
Beneath the dense canopy of a lush rainforest, you resolve to synthesize a serum from a rare and potent flower, its properties unknown to the wider world. Working side by side with an indigenous guide, whose ancestors have stewarded these secrets for generations, you employ the accumulated wisdom of the rainforest to craft the groundbreaking serum. As word of your breakthrough spreads, mercenaries employed by a shadowy corporation descend upon the valley, intent on seizing the serum for their employers. Yet, through cunning and a bit of luck, you and your guide manage to evade their grasp, safeguarding the precious vial.

Having successfully synthesized the serum and faced down the mercenaries' threat, you find yourself at a crossroads. The long-term protection of the valley and its secrets weighs heavily on your mind, compelling you to contemplate the future of the serum and its formula.
+ [Destroy the serum formula] -> RLL
+ [Patent the serum formula] -> RLR
== RLL ==
After a long period of contemplation and the weight of responsibility heavy on your shoulders, you make a pivotal decision to destroy the serum formula. It's a secret too potent and dangerous for any one person or entity to wield. The realization dawns on you that some of nature's secrets are meant to be preserved, not exploited, grounding you in a new truth.

With a renewed sense of purpose and urgency, you begin to advocate for the sustainable research and conservation of the Amazon. Recognizing its unparalleled biodiversity and the critical role it plays in the global ecosystem, you see this as a pivotal step in ensuring a safer, more balanced world.
-> END
== RR ==
You've decided to delve deep into the archives of ancient technologies, unearthing secrets that modern science might have overlooked in the quest for sustainable energy solutions. Your curiosity leads you to discover an old map, pointing towards a long-lost city. This city, according to historical texts, was light years ahead of its time, powered entirely by an extraordinary crystal capable of harnessing solar energy more efficiently than anything current technology could dream of.

Your excitement is soon overshadowed by a troubling revelation. You learn of a powerful tech conglomerate's sinister plan to capture this crystal, aiming to monopolize its potential for profit rather than the betterment of humanity. The thought of such a groundbreaking discovery falling into the wrong hands lightens a fire within you.

You're acutely aware of the crystal's immense power and the conglomerate's intentions. The imperative now is to protect this ancient technology from exploitation while ensuring its benefits can be shared globally, thereby revolutionizing the world's energy sources.
+ [Replicate and campaign] -> RRL
+ [Negotiate with conglomerate] -> RRR
== RRL ==
After discovering an ancient crystal with remarkable energy capabilities, you decide it's too important to keep it hidden or for exclusive use. The potential for a global green technology revolution sparks an idea, and you set your sights on replicating its technology for widespread, sustainable use.

With the assistance of your trusted allies, you dive into ancient manuscripts and decrypt the secrets of replicating the crystal's energy capabilities. Knowing that a powerful conglomerate is on your heels, wanting this technology for themselves, you cleverly set up decoys across the globe to throw them off your scent.

Your efforts culminate in the launch of a pioneering campaign, promoting the integration of this ancient wisdom with modern green technology. The campaign is a hit, drawing attention worldwide and positioning you as a leader in global sustainability efforts. Now, it's about maintaining this momentum and safeguarding the technology from those who wish to exploit it.
-> END
== RRR ==
Driven by an unwavering desire to combat pollution, you set out on a quest to find a natural purifier, journeying into uncharted territories. Your explorations lead you deep into a remote forest, where, by chance or fate, you stumble upon a hidden cave system, inviting yet unexplored. Venturing further inside, your curiosity is rewarded when you discover a previously unknown bioluminescent plant species. This remarkable flora possesses the ability to purify air at an unprecedented rate, holding promise as a revolutionary solution to the world’s pollution crisis.

Standing before this glowing marvel, you realize the potential impact of your discovery. You're faced with a decision on how to proceed with this groundbreaking find.
-> END
== RLR ==
Feeling an urgent need to address the world's clean water crisis, you decide to fund and lead an expedition to discover a mythical tree known for its water purifying capabilities. Along the way, you ally with a local conservationist who knows the area well. However, your noble mission soon faces opposition from a powerful corporation with plans to monopolize water resources. Despite the hurdles, both natural and manufactured by your corporate adversaries, your persistence pays off when you finally discover the tree. Inspired by this success, you don't stop there and initiate a worldwide campaign to protect this miraculous tree and promote its sustainable use for water purification. Your efforts eventually lead to a groundbreaking advancement in clean water access and more environmentally friendly conservation practices globally.
-> END
== LR ==
As you venture deep into the rich, untamed rainforest, your aim is not only to locate resources but also to seek assistance in your endeavors. The dense foliage breaks open to reveal a captivating sight: a rare plant that radiates with a vitality that suggests it possess spectacular healing properties. However, your discovery quickly turns bittersweet as you learn about a ruthless pharmaceutical company's plans to claim the plant for themselves, regardless of the consequences to the ecosystem or the indigenous people who depend on it.

Informed of the pharmaceutical company's intentions for the rare plant, you find yourself facing a predicament. Your goal is now to safeguard this remarkable species and support the local communities, ensuring the plant's benefits are shared ethically and sustainably.
+ [Synthesize plant compound] -> LRL
+ [Negotiate with company] -> LRR
== LRL ==
In a moment of brilliance, you decide to synthesize the plant's unique compound using your portable lab equipment. It's a challenging process, but your expertise and the equipment's advanced capabilities are up to the task. 
Next, you find yourself side by side with the indigenous community, defending this rare plant from a group of pharmaceutical mercenaries. It's a tense situation, but together, you manage to protect this natural treasure. 
Finally, after ensuring the compound's secrets are safe, you send all the synthesized compound's data to a colleague you trust implicitly. It's a critical step to ensure that the knowledge doesn't fall into the wrong hands and can be used for the greater good.
-> END
== LRR ==
Deciding to lead an expedition to Antarctica, your hunger for innovation and discovery propels you into the frozen unknown. As you navigate the icy expanses, you uncover something truly remarkable—a prehistoric plant with the capability to purify heavily polluted water. News of this groundbreaking discovery quickly spreads, capturing the attention of a powerful energy corporation. They see not the potential for environmental salvation, but a tool to be exploited for their own gain.

In this pivotal moment, you realize the weight of responsibility resting on your shoulders. The potential to change the world for the better is within grasp, but so too is the threat of allowing such a precious discovery to fall into the wrong hands. The decision you make next could shape the fate of the planet.
-> END
== LLR ==
Amidst a sudden and violent attack on your laboratory, you find yourself backed into a corner, with one last, desperate gamble left. Ignoring the risks, you inject yourself with an experimental serum that grants superhuman abilities. The effects are instantaneous, endowing you with strength, speed, and resilience far beyond any human. 
Using these newfound powers, you fight off the attackers with a ferocity that surprises even yourself. As the dust settles and the last of your assailants flees, you vow to protect your research and use your gifts for a greater cause. 
Months later, leveraging your inventions in ways previously unimaginable, you introduce a groundbreaking clean energy technology to the world. This not only secures your legacy but also transforms the future of energy consumption, setting a new path towards sustainability and environmental preservation.
-> END
`;
