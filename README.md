 Simulation Paris-Saclay-Aeroport
 
 Notre programme simulant la piste d'atterrissage d’un aéroport fonctionne sur le
 concept théorique de structure de données TAS. Selon ces derniers soit l'élément le plus
 petit ou le plus grand se retrouve en première position , et dans ses sous branches se
 trouvent respectivement soit des éléments plus grands soit uniquement des éléments plus
 petits.
 
 Dans notre cas, les éléments présents dans le tas de l'aéroport sont des avions. Les
 avions sont des objets que nous avons créés possédant les attributs :
 
 ● indicatif : un Str composé de 3 lettres prises au hasard et de 3 chiffres également
 pris au hasard , ce qui rend cet indicatif quasi unique.
 
 ● autonomie : un int indiquant le nombre d’heure que l’avion peut encore voler , nous
 permettant ainsi de les comparer par la suite.
 
 ● Pirate : Un Booléen indiquant si l’avion est sous l’emprise de pirate de l’air
 
 ● En_feu : UnBooléen indiquant si le l’avion est au prise avec un feu déclaré dans ses
 moteurs
 
 ● temps_pirate : un attribut initialisé à 0 indiquant depuis combien de temps les pirates
 sont présents dans l’avion.
 Cette classe possède ses propres méthodes dont priorités et less than , qui nous permet de
 comparer les avions basées sur les critères suivants:
 La priorité est égale au nombre d’autonomie de l’avion , ou si il est en feu il vaut-10000 et si
 il y a des pirates on soustrait 5 a sa priorité définie plus haut.
 Lorsque l’on lance le jeu on crée une liste d’avions qu’on va transformer en tas grâce à une
 fonction et on va stocker les résultats dans un objet aéroport. Les fonctions vont se baser
 sur l’objet aéroport pour bien fonctionner.
 
 Lors de la simulation on enlève l’avion au plus haut dans le tas , donc le plus petit
 avion , ou bien l’avion prioritaire. Cependant nous avons ajouté quelques éléments à cette
 partie du code. Notamment que lors d’un tour les avions présent dans le tas peuvent être
 pirate ou bien un feu se déclare , selon des probabilité initialisée à 0.05 mais pouvant être
 modifié (nous avion pensez à ajouter une extension météo augmentant les probabilité d’un
 feu se déclarant dans l’avion si la météo était à l'orage). Pour s’assurer que le paradigme
des tas soit toujours vérifiée on actualise le tas en faisant remonter les éléments pirate ou
 ayant pris feu durant le tour;
 
 De plus, nous avons implémenté un système de hangar mais nous n'avons pas
 adapté l'interface graphique.Voici le fonctionnement des hangars:
 Un aéroport possède plusieurs hangars dans lesquels les avions peuvent être
 stockés après l'atterrissage. Il faut donc que le hangar soit libre pour qu'un avion
 puisse atterrir sinon il n'aura nul part où être stocké. Une fois dans le hangar, un
 avion prend X heure avant qu'il libère la place. Donc dans certaines situations les
 avions ne peuvent pas atterrir parce que tous les hangars sont pris, il doit attendre
 quelques heures qu'il se libère.De plus si l’avion est en feu , il prend une heure de
 plus dans le hangar le temps que les pompiers éteignent le feu.
 
 A la fin de la journée (fin de la simulation : la taille du tas est égale a 0), on vous
 propose d'arrêter le jeu ou bien de recommencer une nouvelle journée de travail avec de
 nouveaux avions. Si vous arreter le jeu le programme se termine.
 Nous avons accompagné tout notre projet d’une interface graphique présentant un clipboard
 s’actualisant chaque tour et indiquant l’ordre des premiers avions qui vont atterrir. De plus,
 sur la droite de l'écran se trouve une animation des avions atterrissant. Cependant l’interface
 n'est pas à jour, elle affichera un avion qui atterri mais il n'y aura aucun changement dans le
 tas d'atterrissage et donc sur le clipboard.
 
 Ce projet nous a permis de mieux approfondir la complexité de la structure théorique des tas
 et permis de retravailler en groupe et sur les classes. Cependant il nous reste plein d’idées
 pour améliorer notre simulation comme une animation plus fluide, une animation de Hijack
 ou bien une extension météo
