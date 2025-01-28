# RECYCLE W4R - AR Edition
Jeu réalisé dans le cadre d'un projet IG3 Image&Interaction, à Polytech Montpellier.  

RECYCLE W4R - AR Edition est un jeu de recyclage de type ”fruit basket”. Différents déchets tombent du haut de
l’écran, et le joueur doit rattraper le déchet à l’aide de la bonne poubelle.  

Le type de poubelle change selon notre disposition de doigts, et les poubelles suivent nos mains.  

Certains déchets sont composés de plusieurs parties qui ne se jettent pas forcément dans la
même poubelle, donc on pourra ”slice” avec notre main pour découper l’objet en plusieurs parties.  

Chaque déchet collecté ajoute des points de score, et se tromper nous en fait perdre et nous
enlève une vie. Le joueur a de base 3 vies et peut potentiellement en regagner grâce à des bonus.  

A la fin de la partie, un leaderboard apparaît, et des statistiques sur notre recyclage apparaissent.


# Prérequis

- Python 3.8 à 3.12 (inclu)
- pip (pour installer des dépendances)
- Bibliothèques Python :
  - `time`
  - `cv2`
  - `enum`
  - `os`
  - `typing`
  - `datetime`
  - `csv`
  - `copy`
  - `random`
- Dépendances :
  - `PIL`
  - `scipy`
  - `mediapipe`
  - `numpy`
  - `requests`
# Installation

Clonez ce dépôt sur votre machine locale :
   ```bash
   git clone https://github.com/ton-utilisateur/recycle-w4r.git
   cd recycle-w4r
  ```
## Ou
Environnement virtuel (Prérequis : avoir Conda) : clonez le dépot (voir plus haut), puis sur votre terminal :  
```bash
conda env create -f environment.yml
```
Sur VsCode : Ctrl - Shift - P : Python:Select Interpreter et choisir l'environnement du projet.  
Si vous avez l'erreur : no module 'requests', tapez manuellement dans votre terminale la commande  
```bash
conda install -c conda-forge requests
```
Si vous etes avec Conda.  
Cela devrait fonctionner.  
# Utilisation

Lancez le jeu avec la commande suivante :

```bash
python main.py
```

# Lien utiles pour le développement
- [Projet Overleaf](https://www.overleaf.com/project/677cd396395cb682428043f3)
- [Lien création UML](https://draw.io)
- [Lien Diagramme de Gant](https://docs.google.com/spreadsheets/d/1lN4seDiW93CPrhIQoiOF3anqnDFao1mGMybjAvzFJxA/)

# Auteurs :
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%">
        <a href="https://github.com/Byxis">
          <img src="https://avatars.githubusercontent.com/u/35427808?v=4" width="100px;" alt="Alexis"/>
          <br />
          <sub>
            <b>Alexis Serrano</b>
            <br />
          </sub>
        </a>
        <br />
        <a href="https://github.com/Byxis/IG3-ASAIoT/commits/?author=Byxis" title="Commits">Commits</a>
        <br />
        <a href="https://github.com/Byxis/IG3-ASAIoT/pulls?q=is%3Apr+author%3AByxis" title="Reviewed Pull Requests">Reviewed Pull Requests</a>
         <td align="center" valign="top" width="14.28%">
        <a href="https://github.com/SymetTr1x">
          <img src="https://avatars.githubusercontent.com/u/190523592?v=4" width="100px;" alt="Tom"/>
          <br />
          <sub>
            <b>Tom Leardi</b>
            <br />
          </sub>
        </a>
        <br />
        <a href="https://github.com/Byxis/IG3-ASAIoT/commits/?author=SymetTr1x" title="Commits">Commits</a>
        <br />
        <a href="https://github.com/Byxis/IG3-ASAIoT/pulls?q=is%3Apr+author%3ASymetTr1x" title="Reviewed Pull Requests">Reviewed Pull Requests</a>
         <td align="center" valign="top" width="14.28%">
        <a href="https://github.com/Askneuh">
          <img src="https://avatars.githubusercontent.com/u/81713112?v=4" width="100px;" alt="Seb"/>
          <br />
          <sub>
            <b>Sébastien Pinta</b>
            <br />
          </sub>
        </a>
        <br />
        <a href="https://github.com/Byxis/IG3-ASAIoT/commits/?author=Askneuh" title="Commits">Commits</a>
        <br />
        <a href="https://github.com/Byxis/IG3-ASAIoT/pulls?q=is%3Apr+author%3AAskneuh+" title="Reviewed Pull Requests">Reviewed Pull Requests</a>        
    </tr>
  </tbody>
</table>
