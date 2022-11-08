from dynamixel_sdk import *


def verify_goal_position(goal, goal_max, goal_min):
    """
    Verfica se a posição desejada é válida;
    :param goal: Posição desejada.
    :param goal_max: Posição máxima válida.
    :param goal_min: Posição mínima válida.
    :return:
    """
    if goal > goal_max:
        print('Objeto saiu do campo máximo de visão.')
        return goal_max
    elif goal < goal_min:
        print('Objeto saiu do campo mínimo de visão.')
        return goal_min
    else:
        return goal


class VigilantMotors:

    def __init__(self):

        # =======================
        #        Motor X
        # =======================

        self.DXL_ID_X = 1
        self.goal_max_x = 3000
        self.goal_min_x = 1150
        self.goal_x = 2120
        self.center_x = 320

        # =======================
        #       Motor Y
        # =======================

        self.DXL_ID_Y = 2
        self.goal_max_y = 2400
        self.goal_min_y = 1800
        self.goal_y = 2100
        self.center_y = 240

        # =======================
        #    MX106 VARIABLES
        # =======================

        # Control table address
        self.ADDR_MX_TORQUE = 24
        self.ADDR_MX_GOAL_POSITION = 30
        self.ADDR_MX_PRESENT_POSITION = 36

        # Protocol version
        self.PROTOCOL_VERSION = 1.0

        self.BAUDRATE = 57600
        self.DEVICE = '/dev/ttyACM0'

        self.TORQUE_ENABLE = 1
        self.TORQUE_DISABLE = 0

        self.TargetRange = 40  # (min > 3)

        self.portHandler = PortHandler(self.DEVICE)
        self.packetHandler = PacketHandler(self.PROTOCOL_VERSION)

        # Open port
        self.portHandler.openPort()

        # Set port baudrate
        self.portHandler.setBaudRate(self.BAUDRATE)

        self.initiate_motor()

    def initiate_motor(self):
        """
        Vai para a posição inicial;
        :return:
        """
        print('Iniciando motores.')
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID_X, 28, 6)  # P
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID_X, 27, 1)  # I
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID_X, 26, 100)  # D

        # PID Y
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID_Y, 28, 6)  # P
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID_Y, 27, 1)  # I
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID_Y, 26, 100)  # D

        while True:
            self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID_X, self.ADDR_MX_GOAL_POSITION, self.goal_x)

            self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID_Y, self.ADDR_MX_GOAL_POSITION, self.goal_y)

            self.get_present_pos()
            # Verifica se chegou ao destino com um range do x;
            if not (abs(self.goal_x - self.dxl_present_position_x) > self.TargetRange):
                print('Posição inicial X.')
                if not (abs(self.goal_y - self.dxl_present_position_y) > self.TargetRange):
                    print('Posição inicial .')
                    break

    def calculate_route(self, coord_x, coord_y):
        """
        Faz o cálculo da coordenada, recebe os valores em pixel
        e retorna as coordenadas que devolve em ângulo para os motores;
        :param coord_x: Valor em pixel da coordenada desejada x;
        :param coord_y: Valor em pixel da coordenada desejada y;
        :return:
        """
        self.get_present_pos()
        self.goal_x = int(self.dxl_present_position_x + (self.center_x - coord_x))
        # verificar
        self.goal_y = int(self.dxl_present_position_y - (self.center_y - coord_y))
        # Verificando a posição de x;
        self.goal_x = verify_goal_position(self.goal_x, self.goal_max_x, self.goal_min_x)
        # Verificando a posição de y;
        self.goal_y = verify_goal_position(self.goal_y, self.goal_max_y, self.goal_min_y)
        print(self.goal_y)

    def get_present_pos(self):
        """
        Pega a posição a localização atual do robô;
        :return:
        """
        dxl_comm_result_x, dxl_comm_result_y = 1, 1

        while dxl_comm_result_x != 0:
            self.dxl_present_position_x, dxl_comm_result_x, dxl_error_x = self.packetHandler.read2ByteTxRx(
                self.portHandler,
                self.DXL_ID_X,
                self.ADDR_MX_PRESENT_POSITION)
        while dxl_comm_result_y != 0:
            self.dxl_present_position_y, dxl_comm_result_y, dxl_error_y = self.packetHandler.read2ByteTxRx(
                self.portHandler,
                self.DXL_ID_Y,
                self.ADDR_MX_PRESENT_POSITION)

    def go_motor(self, coord_x, coord_y):
        """
        Manda o motor ir a posição desejada;
        :return:
        """
        self.calculate_route(coord_x, coord_y)

        while True:
            self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID_X, self.ADDR_MX_GOAL_POSITION, self.goal_x)
            self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID_Y, self.ADDR_MX_GOAL_POSITION, self.goal_y)
            print('Mover para:', self.goal_x)
            self.get_present_pos()
            # Verifica se chegou ao destino com um range do x;
            if not (abs(self.goal_x - self.dxl_present_position_x) > self.TargetRange):
                if not (abs(self.goal_y - self.dxl_present_position_y) > self.TargetRange):
                    print('Chegou ao objetivo.')
                    break
