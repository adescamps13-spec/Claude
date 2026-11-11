# Brief projet : interface brand Electra (prototype)

Ce fichier est le brief de référence du projet. Lis-le en entier avant de faire quoi que ce soit, puis suis la méthode de travail décrite en partie 8.

---

## 1. Ce qu'on construit

Une interface web interne pour la marque Electra (recharge ultra-rapide de véhicules électriques). Elle sert de porte d'entrée unique à tous les marchés européens (France en centrale, puis Belgique, Suisse, Allemagne) pour :

1. faire une demande à l'équipe brand ;
2. retrouver les fondamentaux de la marque à jour ;
3. retrouver et réutiliser les assets déjà produits ;
4. accéder aux assistants IA (adapter, vérifier, ranger).

C'est un **prototype de démonstration**. Il doit être beau, clair et crédible en démo de trois minutes. Il n'a pas besoin de gérer des comptes utilisateurs ni une forte charge.

## 2. Architecture

Trois couches, à respecter strictement :

- **Notion est le back-office.** Toutes les données y vivent. On ne crée aucune autre base de données.
- **L'interface est la vitrine.** Elle lit Notion et affiche. Elle n'écrit dans Notion qu'à un seul endroit : le formulaire de demande.
- **Claude est le poste de pilotage.** Les mises à jour de contenu et les assistants IA se lancent depuis Claude, pas depuis l'interface. Dans ce prototype, l'interface ne fait aucun appel à une IA.

## 3. Le scénario de démo à réussir

L'équipe suisse a besoin d'un ad pour une ouverture de station.

1. Elle ouvre l'interface et dépose une demande via le formulaire.
2. La demande apparaît dans le tableau de bord Notion.
3. Elle va dans la banque d'assets, filtre sur « Ouverture de station » et trouve un ad français qui a performé.
4. Elle voit que cet ad a déjà une déclinaison en allemand, reliée à l'original.
5. Elle ouvre l'assistant « Adapter » pour savoir comment en produire une autre.
6. Elle consulte la grille « on brand » dans le hub de marque.

Chaque étape doit fonctionner sans accroc. Tout ce qui ne sert pas ce scénario est secondaire.

## 4. Choix techniques

- **Next.js** (App Router) avec **TypeScript**.
- **Tailwind CSS** pour le style.
- **SDK officiel Notion** (`@notionhq/client`) pour lire et écrire.
- Hébergement sur **Vercel**, relié au dépôt GitHub dès la phase 0. Chaque modification poussée est mise en ligne automatiquement, et c'est sur cette adresse en ligne que le pilote vérifie le résultat. Rien ne tourne sur son ordinateur.

Contraintes non négociables :

- Le jeton Notion reste **côté serveur**. Il est lu depuis une variable d'environnement `NOTION_TOKEN`. Il n'apparaît jamais dans le code, jamais dans le navigateur, jamais dans un commit, jamais dans cette conversation.
- Le jeton est saisi par le pilote du projet **directement dans les réglages de Vercel**. Ne demande jamais à le voir.
- `.env.local` est dans `.gitignore` dès le départ, au cas où le projet serait un jour lancé en local.
- Les liens vers les fichiers hébergés par Notion **expirent au bout d'une heure environ**. Ne jamais les mettre en cache longtemps : les relire côté serveur à chaque rendu, ou avec une revalidation courte.
- L'API Notion distingue désormais les bases (`database`) et leurs sources de données (`data source`). Les deux identifiants sont fournis en partie 5. **Vérifie dans la documentation Notion actuelle quel identifiant et quelle méthode utiliser avec la version du SDK installée**, au lieu de supposer.
- Les noms de propriétés Notion contiennent des accents et des apostrophes. Utilise-les exactement comme écrits en partie 5.

## 5. Les données Notion

Page racine de la maquette : `415f66520550801ca17cdfa2dce6ee3a`

### 5.1 Demandes brand

- Base : `bcb4624d09d545bbb89417ad8d6fe46e`
- Source de données : `98ac7b49-0f6d-46a7-b637-45421d4cd4a3`

| Propriété | Type | Valeurs |
|---|---|---|
| Demande | titre | |
| Statut | statut | À trier, En cours, En validation, Livré |
| Type de demande | sélection | Création d'assets, Contenu édito, Ads, Traduction / adaptation, Check on brand, Autre |
| Urgence | sélection | Critique, Haute, Normale, Basse |
| Marché | sélection | France, Belgique, Suisse, Allemagne, Autre marché |
| Demandeur | texte | |
| Équipe | sélection | Marketing, Communication, Sales, Produit, RH, Direction |
| Email | e-mail | |
| Deadline | date | |
| Brief | texte | |
| Assigné à | personnes | rempli par la brand team, jamais par le formulaire |
| Livrable | URL | rempli par la brand team |
| Reçue le | date de création | automatique |
| N° | identifiant unique | automatique, préfixe ELBRAND |
| Assets livrés | relation | vers la banque d'assets |

### 5.2 Ressources de marque

- Base : `48ee01789d8b490399134d195a632141`
- Source de données : `d38c2525-8089-4b52-9c6e-ebc1cb8e8d11`

| Propriété | Type | Valeurs |
|---|---|---|
| Ressource | titre | |
| Catégorie | sélection | Plateforme de marque, Messages clés, Boilerplate, Logos, Direction artistique, Brand guidelines, Tone of voice |
| Statut | sélection | À jour, En révision, À compléter |
| Langues disponibles | sélection multiple | FR, NL, DE, IT, EN |
| Version | texte | |
| Validée le | date | |
| Responsable | personnes | |
| Résumé | texte | |
| Fichier | fichiers | |
| Lien | URL | |

Le contenu de chaque ressource est dans le **corps de la page Notion** (titres, paragraphes, listes, encadrés). Il faut le lire bloc par bloc et le rendre proprement.

### 5.3 Banque d'assets

- Base : `e69e403249df4df0b3d6a2d4948bcb9e`
- Source de données : `31f73a1a-5d72-45a2-ae34-1e648ac11747`

| Propriété | Type | Valeurs |
|---|---|---|
| Asset | titre | |
| Type d'asset | sélection | Ad, Kakémono, Affichage, Print, Post social, Vidéo de marque, Présentation |
| Visuel | fichiers | peut être vide |
| Statut | sélection | À valider, Validée, Archivée |
| Campagne | texte | |
| Type de message | sélection | Notoriété de marque, Ouverture de station, Vitesse de recharge, Prix, App et expérience, B2B et flottes, Marque employeur, Carte de recharge, Abonnement Electra+, Offre de bienvenue |
| Marché | sélection | France, Belgique, Suisse, Allemagne, Autre marché |
| Langue | sélection | FR, NL, DE, IT, EN |
| Format | sélection multiple | 1:1, 4:5, 9:16, 16:9, 4:3, 3:4 |
| Canal | sélection multiple | Meta, LinkedIn, YouTube, TikTok, Display, DOOH |
| Nature | sélection | Image, Vidéo, Carrousel, PDF |
| Date de production | date | |
| Score de perf | nombre | de 0 à 100, peut être vide |
| CTR (%) | nombre | peut être vide |
| Impressions | nombre | peut être vide |
| Coût par clic (€) | nombre | peut être vide |
| ID plateforme pub | texte | |
| Lien public | URL | |
| Fichier source | URL | |
| Source | sélection | Réelle, Démo |
| Adaptée de | relation | vers l'asset d'origine, dans la même base |
| Déclinaisons | relation | inverse de « Adaptée de » |
| Demande d'origine | relation | vers Demandes brand |

Certaines fiches ont aussi un court texte dans le corps de la page (message, appel à l'action, diffusion).

### 5.4 Inspiration

- Base : `077cc16803ae40e7ad13da19346306d1`
- Source de données : `0dc6af96-f44a-4a8f-93d8-4605ab375632`

Base vide, prévue pour un temps 2. Ne pas la lire dans ce prototype.

## 6. Les pages

Navigation principale : Accueil, Faire une demande, La marque, Banque d'assets, Assistants, Inspiration.

### 6.1 Accueil

- Une phrase d'accroche : le point d'entrée unique de la marque Electra, pour tous les marchés.
- Quatre grandes entrées vers les espaces : Faire une demande, La marque, Banque d'assets, Assistants.
- Un bloc « Les assets qui performent » : les trois assets validés au meilleur score de perf.

### 6.2 Faire une demande

Formulaire en une page, qui crée une fiche dans « Demandes brand ».

- Champs : objet de la demande (Demande), type de demande, marché, urgence, deadline, nom (Demandeur), équipe, e-mail, brief.
- Ne jamais exposer : Statut, Assigné à, Livrable. Le statut est mis à « À trier » automatiquement.
- Validation : objet, type, marché, nom et e-mail obligatoires. Messages d'erreur clairs, en français.
- Après envoi : un écran de confirmation qui affiche le numéro de la demande (N°) et propose d'en déposer une autre.
- Protéger l'envoi contre le double clic.

### 6.3 La marque

- Une page liste : les sept ressources, présentées comme des cartes, avec catégorie, résumé, statut et langues disponibles.
- Une page détail par ressource : le contenu de la page Notion rendu proprement (titres, paragraphes, listes, encadrés, citations, liens).
- Si le statut n'est pas « À jour », afficher un bandeau discret : « Version de travail ».
- Si le statut est « À compléter » et que la page est vide, afficher un état vide soigné plutôt qu'une page blanche.

### 6.4 Banque d'assets

C'est la page la plus importante.

- **Onglets** : « Bibliothèque globale » d'abord, puis un onglet par type d'asset, dans cet ordre : Ads, Kakémonos, Affichage, Print, Posts sociaux, Vidéos de marque, Présentations.
- **Filtres** combinables : marché, langue, type de message, statut. Les filtres se lisent dans l'adresse de la page, pour qu'un lien filtré puisse être partagé.
- **Tri** : par date de production (par défaut) ou par score de perf.
- **Cartes** : visuel en couverture, nom, type de message, marché, langue, formats, score de perf quand il existe. Sans visuel, afficher un fond neutre soigné avec le type d'asset, jamais une image cassée.
- Par défaut, masquer les assets « Archivée ».
- **Page détail** : visuel en grand, toutes les informations utiles, le texte de la fiche, les chiffres de perf s'ils existent, le lien public, et surtout :
  - un bloc « Déclinaisons » qui liste les assets adaptés de celui-ci ;
  - un bloc « Adapté de » qui renvoie vers l'original ;
  - un bouton « Adapter cet asset » qui mène à la page de l'assistant Adapter.

### 6.5 Assistants

Trois cartes, une par assistant : Adapter, Vérifier, Ranger. Pour chacun :

- à quoi il sert, en une phrase ;
- la demande type à copier, avec un bouton « Copier » ;
- un bouton « Ouvrir Claude » qui ouvre https://claude.ai dans un nouvel onglet ;
- ses limites, en deux ou trois points.

Les textes des trois demandes types :

**Adapter**

```
Adapte l'asset « [nom de l'asset] » de la banque d'assets Electra.
Langue cible : [allemand Suisse / allemand Allemagne / néerlandais Belgique / italien / anglais].
Formats voulus : [9:16, 4:5, 1:1, 3:4, 4:3, 16:9].
Range ensuite chaque déclinaison dans la banque d'assets, reliée à l'asset d'origine, en statut « À valider ».
```

**Vérifier**

```
Vérifie si ce fichier est on brand pour Electra.
Applique la grille des brand guidelines du hub de marque, point par point.
Donne un verdict : on brand, à corriger ou hors marque.
Liste chaque écart avec la correction proposée.
```

**Ranger**

```
Voici un nouvel asset produit par [marché] pour la campagne [nom de la campagne].
Range-le dans la banque d'assets Electra en statut « À valider ».
Renseigne le type d'asset, le type de message, le marché, la langue, le format et la date de production.
Si c'est la déclinaison d'un asset existant, relie-le à l'original.
```

Quand on arrive sur l'assistant Adapter depuis la page d'un asset, le nom de l'asset est déjà inséré dans la demande type.

### 6.6 Inspiration

Une page d'attente soignée : ce que sera cet espace (les posts qui surperforment chez les concurrents et dans l'univers de référence d'Electra), avec la mention « Bientôt ».

## 7. Design

- **Intention** : chaleureux et apaisant. L'identité d'Electra s'inspire des applications de bien-être : du calme, de l'air, de la confiance. Pas d'esthétique technologique froide.
- **Beaucoup d'espace**, peu d'éléments par écran, une hiérarchie typographique nette.
- **Couleurs et typographies** : la charte officielle n'est pas encore disponible. Définis toutes les couleurs, polices et rayons comme **variables CSS dans un seul fichier**, avec une palette neutre et douce par défaut, pour que la vraie charte puisse être branchée en changeant ce seul fichier.
- **Ne pas inventer de logo Electra.** Écrire simplement « Electra » en texte, suivi de « Brand ».
- **Mobile d'abord** : tout doit être confortable sur un téléphone, puis s'élargir sur ordinateur.
- **Interface entièrement en français.**
- Accessibilité de base : contrastes suffisants, navigation au clavier, textes alternatifs.
- États soignés partout : chargement, vide, erreur. Si Notion ne répond pas, afficher un message clair, pas une page plantée.

## 8. Méthode de travail

La personne qui pilote ce projet **n'est pas développeur**. Elle connaît très bien le produit et la marque, pas le code.

- Explique ce que tu fais en français simple, sans jargon, étape par étape.
- Avance **phase par phase**. À la fin de chaque phase, arrête-toi, montre le résultat et attends un accord avant de passer à la suivante.
- Demande avant d'installer un outil sur l'ordinateur.
- Quand une action doit être faite à la main (créer le jeton Notion, par exemple), donne les instructions clic par clic et attends la confirmation.
- Ne modifie jamais la structure des bases Notion. Si une donnée semble manquer, signale-le au lieu de la contourner.

### Les phases

**Phase 0 : préparation**

Tu travailles dans une session en ligne, sur un dépôt GitHub. Le pilote n'a rien d'installé sur son ordinateur et ne lancera rien en local.

1. Créer le projet Next.js dans le dépôt, avec `.gitignore`.
2. Ajouter une page de diagnostic `/diagnostic` qui lit la banque d'assets côté serveur et affiche le nombre de fiches trouvées, ou un message d'erreur lisible si le jeton manque ou si l'accès est refusé. Elle n'affiche jamais le jeton.
3. Guider le pilote, clic par clic, pour :
   - relier le dépôt à Vercel ;
   - créer une intégration interne Notion et partager la page racine de la maquette avec elle ;
   - coller le jeton dans les variables d'environnement de Vercel, sous le nom `NOTION_TOKEN` ;
   - relancer le déploiement.
4. Lui demander d'ouvrir `/diagnostic` sur l'adresse en ligne. Attendu : 19 fiches.

Ne pas aller plus loin tant que ce test ne passe pas. À partir de là, à la fin de chaque phase, indique-lui quelle page ouvrir sur l'adresse en ligne pour vérifier.

**Phase 1 : structure et accueil.** Mise en page générale, navigation, variables de design, page d'accueil.

**Phase 2 : banque d'assets.** Liste, onglets, filtres, tri, page détail avec déclinaisons.

**Phase 3 : la marque.** Liste des ressources et rendu du contenu des pages Notion.

**Phase 4 : formulaire de demande.** Envoi vers Notion, validation, confirmation avec numéro.

**Phase 5 : assistants et inspiration.**

**Phase 6 : finitions et démo.** Retirer la page de diagnostic, puis vérifier le scénario de démo complet sur l'adresse en ligne, sur téléphone et sur ordinateur.

## 9. Hors périmètre du prototype

- Comptes utilisateurs, connexion, droits d'accès.
- Appels à une IA depuis l'interface.
- Dépôt de fichiers depuis l'interface.
- Récupération automatique des performances publicitaires.
- Édition des ressources de marque depuis l'interface.
- Traduction de l'interface dans d'autres langues.

Si l'une de ces fonctions semble utile en cours de route, note-la dans un fichier `IDEES.md` au lieu de la construire.

## 10. Le prototype est terminé quand

- le scénario de démo de la partie 3 se déroule sans accroc sur l'adresse en ligne ;
- une demande déposée par le formulaire apparaît dans Notion avec le statut « À trier » ;
- la banque d'assets affiche les 19 fiches, bien réparties dans leurs onglets ;
- les déclinaisons renvoient à leur original, et l'inverse ;
- tout est lisible et agréable sur un téléphone ;
- le jeton Notion n'apparaît nulle part dans le code ni dans le navigateur.
