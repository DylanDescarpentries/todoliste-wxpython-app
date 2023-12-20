import wx, json
import wx.lib.colourutils
from taches import Tache, ModifierTacheDialog


class TodoApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(TodoApp, self).__init__(*args, **kw)

        # Charger l'icône à partir d'un fichier image (au format .ico sur Windows)
        icon = wx.Icon('logo.png', wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

        self.panel = wx.Panel(self)

        titre_tableau = wx.StaticText(self.panel, label="Vos tâches :", pos=(10, 10))

        # Création des boutons et des id
        self.id_modifier = wx.NewIdRef()
        btn_ajouter = wx.Button(self.panel, id=wx.ID_ANY, label='Ajouter', size=(70, 30))
        btn_supprimer = wx.Button(self.panel, id=wx.ID_ANY, label='Supprimer', size=(70, 30))
        btn_afficher = wx.Button(self.panel, id=wx.ID_ANY, label='Afficher', size=(70, 30))
        btn_modifier = wx.Button(self.panel, id=self.id_modifier, label='Modifier', size=(70, 30))

        #Afficher les données de tâches
        self.list_ctrl = wx.ListCtrl(self.panel, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, 'ID')
        self.list_ctrl.InsertColumn(1, 'Nom de la tâche')
        self.list_ctrl.InsertColumn(2, 'État')

        # Création d'un sizer vertical pour contenir les éléments
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Les boutons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(btn_ajouter, 0, wx.ALL, border=2)
        btn_sizer.Add(btn_supprimer, 0, wx.ALL, border=2)
        btn_sizer.Add(btn_afficher, 0, wx.ALL, border=2)
        btn_sizer.Add(btn_modifier, 0, wx.ALL, border=2)

        sizer.Add(btn_sizer, 0, wx.ALL | wx.EXPAND, border=2)

        # les données sous forme de tableaux
        sizer.Add(titre_tableau, 0, wx.ALL, border=2)
        sizer.Add(self.list_ctrl, 0, 0, border=5)        

        # Menu Barre (les boutons ne sont pas encore défini et non pas d'effet)
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        edit_menu = wx.Menu()

        # Création des boutons dans le menu fichier
        file_menu.Append(wx.ID_EXIT, 'Quitter', 'Quitter l\'application')
        file_menu.Append(wx.ID_ANY, 'Supprimer', 'Supprimer la sélection')

        # Ajouter les boutons au menu principal
        menubar.Append(file_menu, 'Fichier')
        self.SetMenuBar(menubar)

        # Création des boutons dans le menu edit
        edit_menu.Append(wx.ID_CANCEL, 'Annuler', 'Annuler la dernière action')
        edit_menu.Append(wx.ID_CANCEL, 'Rétablir', 'Rétablir la dernière action')
        menubar.Append(edit_menu, 'Edition')
        edit_menu.Append(wx.ID_ANY, 'Copier', 'Copier la selection')
        edit_menu.Append(wx.ID_ANY, 'Couper', 'Couper la selection')
        edit_menu.Append(wx.ID_ANY, 'Coller', 'Coller la selection')
        self.SetMenuBar(menubar)
        

        # Lier les fonctions aux éléments du menu
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.supprimer, id=wx.ID_ANY)
        self.Bind(wx.EVT_MENU, self.annuler, id=wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.modifier, btn_modifier)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.modifier, self.list_ctrl)

        # Définition du sizer pour le panneau
        self.panel.SetSizer(sizer)
        self.panel.Layout()  # Forcer une mise en page

        # Ajustement du sizer pour tenir compte de la barre de menu
        sizer.Fit(self)

        # listes nécessaire au bon fonctionnement des fonctions
        self.liste_taches = []
        self.taches_supprimees = []

        # Définition du sizer pour le panneau
        self.panel.SetSizer(sizer)

        # Association des fonctions aux événements de clic des boutons
        self.Bind(wx.EVT_BUTTON, self.ajouter, btn_ajouter)
        self.Bind(wx.EVT_BUTTON, self.supprimer, btn_supprimer)
        self.Bind(wx.EVT_BUTTON, self.afficher, btn_afficher)

        # Affichage de la fenêtre principale
        self.Show()

        # forcer l'affichage
        self.Layout()


    #Fonction pour interagir avec la base de données
    def sauvegarder_taches(self, fichier):
        with open(fichier, 'w') as f:
            taches_serialisees = [tache.__dict__ for tache in self.liste_taches]
            json.dump(taches_serialisees, f)

    def charger_taches(self, fichier):
        try:
            with open(fichier, 'r') as f:
                donnees = json.load(f)
                self.liste_taches = [Tache(**tache) for tache in donnees]
        except FileNotFoundError:
            # Si le fichier n'existe pas encore, ne faites rien
            print('le fichier est introuvable')
            pass

    # Quitter l'application
    def OnQuit(self, event):
        self.Close()

    #
    def ajouter(self, event):
        # récupérer l'entré utilisateur 
        entree_ajouter = wx.TextEntryDialog(self, 'Entrez une nouvelle tâche :', 'Ajouter une tâche', '')

        # Ajouter la tache à la liste et le sauvegarder
        if entree_ajouter.ShowModal() == wx.ID_OK:
            nom_tache = entree_ajouter.GetValue()
            identifiant = len(self.liste_taches) + 1
            nouvelle_tache = Tache(identifiant, nom_tache)
            self.liste_taches.append(nouvelle_tache)
            self.sauvegarder_taches('datas.json')

            # Message d'alerte pour confirmer la création de la tache
            wx.MessageBox(f"Vous avez ajouté : {nouvelle_tache}", "Info", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Veuillez entrer une description pour la tâche.", "Erreur", wx.OK | wx.ICON_ERROR)
        entree_ajouter.Destroy()



    def supprimer(self, event):
        # recuperer l'element à supprumer
        selected_index = self.list_ctrl.GetFirstSelected()
        if selected_index != -1:
            # Un élément est sélectionné, supprimez-le de la liste
            del self.liste_taches[selected_index]
            self.sauvegarder_taches('datas.json')

            # Mettez à jour l'affichage dans le listCtrl
            self.afficher(event)
        else:
            wx.MessageBox('Veuillez sélectionner une tâche à supprimer.', 'Erreur', wx.OK | wx.ICON_ERROR)


    def afficher(self, event):
        self.list_ctrl.DeleteAllItems()  # Effacer les éléments actuels
        self.charger_taches('datas.json') 
        for index, tache in enumerate(self.liste_taches):
            etat = "complete" if tache.complete else "En cours"
            self.list_ctrl.InsertItem(index, str(tache.id))
            self.list_ctrl.SetItem(index, 1, tache.nom_tache)
            self.list_ctrl.SetItem(index, 2, etat)
        
            # Modifier la couleur d'arrière-plan pour les tâches terminées avec un dégradé
            if tache.complete:
                # Utilisez la couleur de votre choix pour les tâches terminées
                gradient = wx.Colour(144, 238, 144)  # Vert clair
                self.list_ctrl.SetItemBackgroundColour(index, gradient)
            else:
                # Pour les tâches en cours, vous pouvez laisser la couleur par défaut
                self.list_ctrl.SetItemBackgroundColour(index, wx.NullColour)
    
    def annuler(self, event):
        if self.taches_supprimees:
            # Il y a des tâches supprimées, rétablissez la dernière
            derniere_tache_supprimee = self.taches_supprimees.pop()
            self.liste_taches.append(derniere_tache_supprimee)
            self.sauvegarder_taches('datas.json')

            # Mettez à jour l'affichage dans le ListCtrl
            self.afficher(event)
        else:
            wx.MessageBox('Aucune action à annuler.', 'Info', wx.OK | wx.ICON_INFORMATION)

    def modifier(self, event):
        # Obtenez l'index du premier élément sélectionné dans le ListCtrl
        selected_index = self.list_ctrl.GetFirstSelected()

        if selected_index != -1:
            # Récupérer la tâche correspondante dans la liste
            tache = self.liste_taches[selected_index]

            # Afficher une boîte de dialogue pour modifier la tâche
            dlg = ModifierTacheDialog(self, f'Modifier la tâche "{tache.nom_tache}"', tache)

            # Vérifier si l'utilisateur a appuyé sur OK
            if dlg.ShowModal() == wx.ID_OK:
                # Sauvegarder les modifications
                self.sauvegarder_taches('datas.json')

                # Mettre à jour l'affichage dans le ListCtrl
                self.afficher(event)
        else:
            wx.MessageBox('Veuillez sélectionner une tâche à modifier.', 'Erreur', wx.OK | wx.ICON_ERROR)

if __name__ == '__main__':
    app = wx.App(False)
    frame = TodoApp(None, title='Todo App')
    frame.Show()
    app.MainLoop()