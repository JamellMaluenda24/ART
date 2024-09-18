class ControladorPasos:
    @staticmethod
    def abrir_formulario_registro():
        from gui.Menu.Form_registro import RegisterApp
        ventana = RegisterApp()
        return ventana
    
    @staticmethod 
    def abrir_login():
        from main import AplicacionLogin
        ventana = AplicacionLogin()
        return ventana
#################################################################################################################
    @staticmethod
    def abrir_formulario_trabajador_paso1(rut):
        from gui.ArtFormulario.Form_Trabajador.trabajador_form_paso1 import FormularioPaso1Trabajador
        ventana = FormularioPaso1Trabajador(rut)
        return ventana

    @staticmethod
    def abrir_formulario_trabajador_paso2(id_art):
        from gui.ArtFormulario.Form_Trabajador.trabajador_form_paso2 import FormularioPaso2Trabajador
        ventana = FormularioPaso2Trabajador(id_art)
        return ventana
    
    @staticmethod
    def abrir_formulario_trabajador_paso2RC(id_art):
        from gui.ArtFormulario.Form_Trabajador.trabajador_form_paso2RC import FormularioPaso2TrabajadorRC
        ventana = FormularioPaso2TrabajadorRC(id_art)
        return ventana
    
    @staticmethod 
    def abrir_formulario_trabajador_paso3(id_art):
        from gui.ArtFormulario.Form_Trabajador.trabajador_form_paso3 import FormularioPaso3Trabajador
        ventana = FormularioPaso3Trabajador(id_art)
        return ventana
    
    @staticmethod 
    def abrir_formulario_trabajador_paso4(id_art):
        from gui.ArtFormulario.Form_Trabajador.trabajador_form_paso4 import FormularioPaso4Trabajador
        ventana = FormularioPaso4Trabajador(id_art)
        return ventana
    
    @staticmethod 
    def abrir_formulario_trabajador_paso5(id_art):
        from gui.ArtFormulario.Form_Trabajador.trabajador_form_paso5 import FormularioPaso5Trabajador
        ventana = FormularioPaso5Trabajador(id_art)
        return ventana
#################################################################################################################
    @staticmethod
    def abrir_formulario_supervisor_paso1(rut):
        from gui.ArtFormulario.Form_Supervisor.supervisor_form_paso1 import FormularioPaso1Supervisor
        ventana = FormularioPaso1Supervisor(rut)
        return ventana

    @staticmethod
    def abrir_formulario_supervisor_paso2(id_art):
        from gui.ArtFormulario.Form_Supervisor.supervisor_form_paso2 import FormularioPaso2Supervisor
        ventana = FormularioPaso2Supervisor(id_art)
        return ventana

    def abrir_formulario_supervisor_paso2RC(id_art):
        from gui.ArtFormulario.Form_Supervisor.supervisor_form_paso2RC import FormularioPaso2SupervisorRC
        ventana = FormularioPaso2SupervisorRC(id_art)
        return ventana
    
    @staticmethod
    def abrir_formulario_supervisor_paso3(id_art):
        from gui.ArtFormulario.Form_Supervisor.supervisor_form_paso3 import FormularioPaso3Supervisor
        ventana = FormularioPaso3Supervisor(id_art)
        return ventana
    
    @staticmethod
    def abrir_formulario_supervisor_paso4(id_art):
        from gui.ArtFormulario.Form_Supervisor.supervisor_form_paso4 import FormularioPaso4Supervisor
        ventana = FormularioPaso4Supervisor(id_art)
        return ventana
    
    @staticmethod
    def abrir_formulario_supervisor_paso5(id_art):
        from gui.ArtFormulario.Form_Supervisor.supervisor_form_paso5 import FormularioPaso5Supervisor
        ventana = FormularioPaso5Supervisor(id_art)
        return ventana
#################################################################################################################
    @staticmethod
    def abrir_menu_trabajador():
        from gui.Menu.trabajador_menu import TrabajadorMenuApp
        ventana = TrabajadorMenuApp()
        return ventana
    
    @staticmethod
    def abrir_menu_supervisor():
        from gui.Menu.supervisor_menu import SupervisorMenuApp
        ventana = SupervisorMenuApp()
        return ventana
    
    @staticmethod
    def abrir_menu_admin():
        from gui.Menu.admin_menu import AdminMenuApp
        ventana = AdminMenuApp()
        return ventana
