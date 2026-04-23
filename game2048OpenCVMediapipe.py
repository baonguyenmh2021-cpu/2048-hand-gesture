import math
import random
import time
import threading

import cv2
import mediapipe as mp
import pyautogui
import pygame

pygame.init()

# --------------------- CAI DAT ---------------------
FPS = 60
CHIEU_RONG, CHIEU_CAO = 800, 800
HANG = 4
COT = 4

O_CAO = CHIEU_CAO // HANG
O_RONG = CHIEU_RONG // COT

MAU_VIEN = (187, 173, 160)
DO_DAY_VIEN = 10
MAU_NEN = (205, 192, 180)
MAU_CHU = (119, 110, 101)

PHONG = pygame.font.SysFont("comicsans", 60, bold=True)
PHONG_MENU = pygame.font.SysFont("comicsans", 40, bold=True)
TOC_DO_DI_CHUYEN = 20

CUA_SO = pygame.display.set_mode((CHIEU_RONG, CHIEU_CAO))
pygame.display.set_caption("2048 Voi Theo Doi Tay")

# --------------------- LOP OSO ---------------------
class OSo:
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, gia_tri, hang, cot):
        self.gia_tri = gia_tri
        self.hang = hang
        self.cot = cot
        self.x = cot * O_RONG
        self.y = hang * O_CAO
        self.rong = O_RONG
        self.cao = O_CAO

    def lay_mau(self):
        chi_so_mau = int(math.log2(self.gia_tri)) - 1
        if chi_so_mau >= len(self.COLORS):
            chi_so_mau = -1
        return self.COLORS[chi_so_mau]

    def ve(self, cua_so):
        mau = self.lay_mau()
        pygame.draw.rect(cua_so, mau, (self.x, self.y, self.rong, self.cao))
        text = PHONG.render(str(self.gia_tri), True, MAU_CHU)
        cua_so.blit(
            text,
            (
                self.x + (self.rong - text.get_width()) / 2,
                self.y + (self.cao - text.get_height()) / 2,
            ),
        )

    def dat_vi_tri(self, ceil=False):
        if ceil:
            self.hang = math.ceil(self.y / O_CAO)
            self.cot = math.ceil(self.x / O_RONG)
        else:
            self.hang = math.floor(self.y / O_CAO)
            self.cot = math.floor(self.x / O_RONG)

    def di_chuyen(self, delta):
        dx, dy = delta
        self.x += dx
        self.y += dy


# --------------------- HAM VE ---------------------
def ve_luoi(cua_so):
    # Ve cac duong chia o ngang
    for hang in range(1, HANG):
        y = hang * O_CAO
        pygame.draw.line(cua_so, MAU_VIEN, (0, y), (CHIEU_RONG, y), DO_DAY_VIEN)
    # Ve cac duong chia o doc
    for cot in range(1, COT):
        x = cot * O_RONG
        pygame.draw.line(cua_so, MAU_VIEN, (x, 0), (x, CHIEU_CAO), DO_DAY_VIEN)
    # Ve vien ngoai
    pygame.draw.rect(cua_so, MAU_VIEN, (0, 0, CHIEU_RONG, CHIEU_CAO), DO_DAY_VIEN)


def ve(cua_so, o_so):
    cua_so.fill(MAU_NEN)
    for o in o_so.values():
        o.ve(cua_so)
    ve_luoi(cua_so)
    pygame.display.update()


# --------------------- HAM HO TRO ---------------------
def lay_vi_tri_ngau_nhien(o_so):
    while True:
        hang = random.randrange(0, HANG)
        cot = random.randrange(0, COT)
        if f"{hang}{cot}" not in o_so:
            return hang, cot


def cap_nhat_o_so(cua_so, o_so, ds_o):
    o_so.clear()
    for o in ds_o:
        o_so[f"{o.hang}{o.cot}"] = o
    ve(cua_so, o_so)


def tao_o_so():
    o_so = {}
    for _ in range(2):
        hang, cot = lay_vi_tri_ngau_nhien(o_so)
        o_so[f"{hang}{cot}"] = OSo(2, hang, cot)
    return o_so


def ket_thuc_di_chuyen(o_so):
    if len(o_so) == HANG * COT:
        return "lost"
    hang, cot = lay_vi_tri_ngau_nhien(o_so)
    o_so[f"{hang}{cot}"] = OSo(random.choice([2, 4]), hang, cot)
    return "continue"


def kiem_tra_thua(o_so):
    luoi = [[0 for _ in range(COT)] for _ in range(HANG)]
    for o in o_so.values():
        luoi[o.hang][o.cot] = o.gia_tri
    # Neu con o trong -> chua thua
    for dong in luoi:
        if 0 in dong:
            return False
    # Kiem tra ghep ngang
    for i in range(HANG):
        for j in range(COT - 1):
            if luoi[i][j] == luoi[i][j + 1]:
                return False
    # Kiem tra ghep doc
    for i in range(HANG - 1):
        for j in range(COT):
            if luoi[i][j] == luoi[i + 1][j]:
                return False
    return True


def ve_game_over(cua_so):
    overlay = pygame.Surface((CHIEU_RONG, CHIEU_CAO))
    overlay.set_alpha(180)
    overlay.fill((255, 255, 255))
    cua_so.blit(overlay, (0, 0))
    text_thua = PHONG.render("Game Over", True, (255, 0, 0))
    text_restart = pygame.font.SysFont("comicsans", 40, bold=True).render("Nhan R de choi lai", True, (0, 0, 0))
    cua_so.blit(
        text_thua,
        (
            CHIEU_RONG / 2 - text_thua.get_width() / 2,
            CHIEU_CAO / 2 - text_thua.get_height()
        ),
    )
    cua_so.blit(
        text_restart,
        (
            CHIEU_RONG / 2 - text_restart.get_width() / 2,
            CHIEU_CAO / 2 + 10,
        ),
    )
    pygame.display.update()


def di_chuyen_o_so(cua_so, o_so, dong_ho, huong):
    cap_nhat = True
    khoi = set()

    if huong == "trai":
        ham_sap_xep = lambda x: x.cot
        dao_nguoc = False
        delta = (-TOC_DO_DI_CHUYEN, 0)
        kt_gioi_han = lambda o: o.cot == 0
        lay_o_tiep = lambda o: o_so.get(f"{o.hang}{o.cot - 1}")
        kt_hop_nhat = lambda o, o_tiep: o.x > o_tiep.x + TOC_DO_DI_CHUYEN
        kt_di_chuyen = lambda o, o_tiep: o.x > o_tiep.x + O_RONG + TOC_DO_DI_CHUYEN
        ceil_flag = True
    elif huong == "phai":
        ham_sap_xep = lambda x: x.cot
        dao_nguoc = True
        delta = (TOC_DO_DI_CHUYEN, 0)
        kt_gioi_han = lambda o: o.cot == COT - 1
        lay_o_tiep = lambda o: o_so.get(f"{o.hang}{o.cot + 1}")
        kt_hop_nhat = lambda o, o_tiep: o.x < o_tiep.x - TOC_DO_DI_CHUYEN
        kt_di_chuyen = lambda o, o_tiep: o.x + O_RONG + TOC_DO_DI_CHUYEN < o_tiep.x
        ceil_flag = False
    elif huong == "len":
        ham_sap_xep = lambda x: x.hang
        dao_nguoc = False
        delta = (0, -TOC_DO_DI_CHUYEN)
        kt_gioi_han = lambda o: o.hang == 0
        lay_o_tiep = lambda o: o_so.get(f"{o.hang - 1}{o.cot}")
        kt_hop_nhat = lambda o, o_tiep: o.y > o_tiep.y + TOC_DO_DI_CHUYEN
        kt_di_chuyen = lambda o, o_tiep: o.y > o_tiep.y + O_CAO + TOC_DO_DI_CHUYEN
        ceil_flag = True
    elif huong == "xuong":
        ham_sap_xep = lambda x: x.hang
        dao_nguoc = True
        delta = (0, TOC_DO_DI_CHUYEN)
        kt_gioi_han = lambda o: o.hang == HANG - 1
        lay_o_tiep = lambda o: o_so.get(f"{o.hang + 1}{o.cot}")
        kt_hop_nhat = lambda o, o_tiep: o.y < o_tiep.y - TOC_DO_DI_CHUYEN
        kt_di_chuyen = lambda o, o_tiep: o.y + O_CAO + TOC_DO_DI_CHUYEN < o_tiep.y
        ceil_flag = False

    while cap_nhat:
        dong_ho.tick(FPS)
        cap_nhat = False
        ds_o = sorted(o_so.values(), key=ham_sap_xep, reverse=dao_nguoc)

        for i, o in enumerate(ds_o):
            if kt_gioi_han(o):
                continue
            o_tiep = lay_o_tiep(o)

            if not o_tiep:
                o.di_chuyen(delta)

            elif (o.gia_tri == o_tiep.gia_tri and o not in khoi and o_tiep not in khoi):
                if kt_hop_nhat(o, o_tiep):
                    o.di_chuyen(delta)
                else:
                    o_tiep.gia_tri *= 2
                    ds_o.pop(i)
                    khoi.add(o_tiep)

            elif kt_di_chuyen(o, o_tiep):
                o.di_chuyen(delta)
            else:
                continue

            o.dat_vi_tri(ceil_flag)
            cap_nhat = True
            
        cap_nhat_o_so(cua_so, o_so, ds_o)

    return ket_thuc_di_chuyen(o_so)


def hien_thi_menu(cua_so):
    chay = True
    mode = None
    while chay:
        cua_so.fill(MAU_NEN)
        tieu_de = PHONG.render("Chon che do choi", True, MAU_CHU)
        option1 = PHONG_MENU.render("1. Su dung ban phim", True, MAU_CHU)
        option2 = PHONG_MENU.render("2. Theo doi tay (Webcam)", True, MAU_CHU)
        option3 = PHONG_MENU.render("3. Thoat game", True, MAU_CHU)
        cua_so.blit(
            tieu_de,
            (CHIEU_RONG/2 - tieu_de.get_width()/2, CHIEU_CAO/3 - tieu_de.get_height()/2)
        )
        cua_so.blit(
            option1,
            (CHIEU_RONG/2 - option1.get_width()/2, CHIEU_CAO/2)
        )
        cua_so.blit(
            option2,
            (CHIEU_RONG/2 - option2.get_width()/2, CHIEU_CAO/2 + 50)
        )
        cua_so.blit(
            option3,
            (CHIEU_RONG/2 - option3.get_width()/2, CHIEU_CAO/2 + 100)
        )
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                chay = False
                mode = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = "keyboard"
                    chay = False
                elif event.key == pygame.K_2:
                    mode = "webcam"
                    chay = False
                elif event.key == pygame.K_3:
                    mode = "exit"
                    chay = False
    return mode


def dem_nguoc(cua_so):
    for i in range(3, 0, -1):
        cua_so.fill(MAU_NEN)
        dem_text = PHONG.render(str(i), True, MAU_CHU)
        cua_so.blit(
            dem_text,
            (
                CHIEU_RONG/2 - dem_text.get_width()/2,
                CHIEU_CAO/2 - dem_text.get_height()/2
            )
        )
        pygame.display.update()
        pygame.time.delay(1000)


def chinh(cua_so):
    dong_ho = pygame.time.Clock()
    chay = True
    thua = False
    o_so = tao_o_so()

    while chay:
        dong_ho.tick(FPS)
        for sukien in pygame.event.get():
            if sukien.type == pygame.QUIT:
                chay = False
                break
            if sukien.type == pygame.KEYDOWN:
                if not thua:
                    if sukien.key == pygame.K_LEFT:
                        di_chuyen_o_so(cua_so, o_so, dong_ho, "trai")
                    elif sukien.key == pygame.K_RIGHT:
                        di_chuyen_o_so(cua_so, o_so, dong_ho, "phai")
                    elif sukien.key == pygame.K_UP:
                        di_chuyen_o_so(cua_so, o_so, dong_ho, "len")
                    elif sukien.key == pygame.K_DOWN:
                        di_chuyen_o_so(cua_so, o_so, dong_ho, "xuong")
                    if kiem_tra_thua(o_so):
                        thua = True
                if sukien.key == pygame.K_r:
                    o_so = tao_o_so()
                    thua = False
        ve(cua_so, o_so)
        if thua:
            ve_game_over(cua_so)
    pygame.quit()


def theo_doi_tay():
    mp_hands = mp.solutions.hands
    mp_ve = mp.solutions.drawing_utils
    cam = cv2.VideoCapture(0)
    truoc_x, truoc_y = 0, 0
    thoi_gian_cuoi = 0
    DO_TRE_LENH = 0.5  # Do tre giua cac lenh (giay)
    NGUONG = 30       # Nguong phat hien chuyen dong (pixel)
    with mp_hands.Hands(
        static_image_mode=False,
        model_complexity=0,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as hands:
        while cam.isOpened():
            ret, khung = cam.read()
            if not ret:
                break
            khung = cv2.flip(khung, 1)
            rgb = cv2.cvtColor(khung, cv2.COLOR_BGR2RGB)
            ket_qua = hands.process(rgb)
            if ket_qua.multi_hand_landmarks:
                for hand_landmarks in ket_qua.multi_hand_landmarks:
                    mp_ve.draw_landmarks(
                        khung,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_ve.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                        mp_ve.DrawingSpec(color=(0, 255, 0), thickness=2),
                    )
                    index_diem = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    h, w, _ = khung.shape
                    x_hien = int(index_diem.x * w)
                    y_hien = int(index_diem.y * h)
                    if truoc_x != 0 or truoc_y != 0:
                        dx = x_hien - truoc_x
                        dy = y_hien - truoc_y
                        khoang_cach = math.hypot(dx, dy)
                        thoi_gian_hien = time.time()
                        if khoang_cach > NGUONG and (thoi_gian_hien - thoi_gian_cuoi) > DO_TRE_LENH:
                            if abs(dx) > abs(dy):
                                if dx > 0:
                                    pyautogui.press("right")
                                    print("Da bam: phai")
                                else:
                                    pyautogui.press("left")
                                    print("Da bam: trai")
                            else:
                                if dy > 0:
                                    pyautogui.press("down")
                                    print("Da bam: xuong")
                                else:
                                    pyautogui.press("up")
                                    print("Da bam: len")
                            thoi_gian_cuoi = thoi_gian_hien
                    truoc_x, truoc_y = x_hien, y_hien
            cv2.imshow("Theo doi tay", khung)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    cam.release()
    cv2.destroyAllWindows()


def main(cua_so):
    che_do = hien_thi_menu(cua_so)
    if che_do == "webcam":
        t_tracking = threading.Thread(target=theo_doi_tay, daemon=True)
        t_tracking.start()
    elif che_do == "exit":
        pygame.quit()
        return
    dem_nguoc(cua_so)
    chinh(cua_so)


if __name__ == "__main__":
    main(CUA_SO)