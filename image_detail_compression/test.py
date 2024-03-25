import cv2
import numpy as np
from xml.dom.minidom import getDOMImplementation


def find_contour(image):
    # 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 이진화 (흰색 영역을 찾기 위함)
    _, binary = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)

    # findContours를 이용하여 흰색 영역의 외곽선 찾기
    contours, _ = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 외곽선이 그려진 이미지 생성 (검정색 배경에 흰색 외곽선)
    contour_img = np.zeros_like(image)
    cv2.drawContours(contour_img, contours, -1, (255, 255, 255), 1)

    return contours, contour_img


def create_svg_path(contours):
    """
    Convert contours to a single SVG path string.
    """
    path_data = " ".join(f"M{c[0][0][0]},{c[0][0][1]} " + " ".join(
        f"L{x[0][0]},{x[0][1]}" for x in c[1:]) for c in contours)
    return path_data + " Z"


def save_svg(filename, path_data, width, height):
    """
    Save a SVG path string to a file.
    """
    impl = getDOMImplementation()
    svg = impl.createDocument("http://www.w3.org/2000/svg", "svg", None)
    svg_elem = svg.documentElement
    svg_elem.setAttribute("width", str(width))
    svg_elem.setAttribute("height", str(height))
    svg_elem.setAttribute("xmlns", "http://www.w3.org/2000/svg")
    path_elem = svg.createElement("path")
    path_elem.setAttribute("d", path_data)
    path_elem.setAttribute("fill", "none")
    path_elem.setAttribute("stroke", "black")
    svg_elem.appendChild(path_elem)
    with open(filename, "w") as f:
        svg.writexml(f)


def simplify_contour_N_save_svg(contours, svg_filename='contour_image.svg'):
    # 각 윤곽선에 대해 approxPolyDP를 사용하여 단순화
    # epsilon = 0.005 * cv2.arcLength(contours[0], True)
    epsilon = 1 * cv2.arcLength(contours[0], True)
    approx_contours = [cv2.approxPolyDP(c, epsilon, True) for c in contours]

    # SVG 경로 데이터 생성
    svg_path_data = create_svg_path(approx_contours)

    # SVG 파일 저장
    save_svg(svg_filename, svg_path_data, image.shape[1], image.shape[0])


def simplify_contour(img, contours):
    for cnt in contours:
        hull = cv2.convexHull(cnt)  # convex hull 추출
        cont_img = cv2.drawContours(img, [hull], 0, (0, 0, 255), 2)
    return cont_img


if __name__ == "__main__":
    # 이미지 파일 로드
    image = cv2.imread('new_0.jpg')

    # 결과 이미지 저장
    output_path = 'contour_image.png'
    contours, contour_img = find_contour(image)
    cv2.imwrite(output_path, contour_img)

    # 결과 이미지 저장
    output_path = "smooth_contour_image.png"
    cont_img = simplify_contour(image, contours)
    cv2.imwrite(output_path, cont_img)

    # 결과 이미지 저장
    # svg_filename = 'contour_image.svg'
    # simplify_contour_N_save_svg(contours, svg_filename)
