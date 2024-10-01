import time
import json
import base64
import requests
import flet as ft


IMG_COLOR_COMPARE_THRESHOLD = 70
IMG_STRUCTURE_COMPARE_THRESHOLD = 35


def fetch_compute(img_in):
    url = 'http://127.0.0.1:8000/predict'
    image_path = img_in
        
    else:
        try:
            with open(image_path, 'rb') as img_file:
                files = {'image': img_file}
                response = requests.post(url, files=files, verify=False)
                
                if response.status_code == 200:
                    response_data = response.json()
                    prediction = response_data['prediction']
                    img_hex = response_data['image']
                    sim = response_data['sim']
                    ssim = response_data['ssim']
                    img_bytes = bytes.fromhex(img_hex)
                    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                else:
                    prediction, img_base64, sim, ssim = 'Error: Server', 'Error: Server', 'Error: Server', 'Error: Server'
                    
        except Exception as err:
            prediction, img_base64, sim, ssim = f'Error: {err}', f'Error: {err}', f'Error: {err}', f'Error: {err}'
    
        
    return prediction, img_base64, sim, ssim


def main(page: ft.Page):
    def run_demo(e):
        container.visible = True
        progress_bar.value = 0.2
        page.update()
        
        img_in = 'assets/51.jpg'
        pred, ib, sim, ssim = fetch_compute(img_in)
        
        if 'Error' in pred:
            myresult.controls.clear()
            myresult.controls.append(
                ft.Text(f'Server is not Reachable! Please try again Later!', size=20)
            )
            container.visible = False
            page.update()
            
        elif int(sim*100) < IMG_COLOR_COMPARE_THRESHOLD or int(ssim*100) < IMG_STRUCTURE_COMPARE_THRESHOLD:
            myresult.controls.clear()
            myresult.controls.append(
                ft.Text(f'Invalid Image! Please try again!', size=20)
            )
            container.visible = False
            page.update()
            
        else:
            progress_bar.value = 0.8
            page.update()
            # Update the displayed image:
            with open(img_in, "rb") as image_file:
                image_data = image_file.read()
                base64_string = base64.b64encode(image_data).decode('utf-8')
            img_width = page.width * 0.5
            aspect_ratio = 16 / 10
            img_height = img_width / aspect_ratio
            time.sleep(0.2)
            
            myresult.controls.clear()
            myresult.controls.append(
                ft.Row([
                    ft.Image(src_base64=base64_string, width=img_width, height=img_height, fit=ft.ImageFit.CONTAIN, border_radius=ft.border_radius.all(5)),
                    ft.Image(src_base64=ib, width=img_width, height=img_height, fit=ft.ImageFit.CONTAIN, border_radius=ft.border_radius.all(5))
                ], alignment=ft.MainAxisAlignment.CENTER)
            )
            progress_bar.value = 0.9
            page.update()
            
            myresult.controls.append(ft.Divider())
            myresult.controls.append(
                ft.Text(f'Creatinine Level: {pred.capitalize()}', size=20, height=60)
            )
            myresult.controls.append(
                    ft.Divider()
            )
            myresult.controls.append(
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Creatinine Level", text_align='center')),
                            ft.DataColumn(ft.Text("Creatinine Range (mg/dL)", text_align='center'))
                        ],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("Low", text_align='center')),
                                    ft.DataCell(ft.Text("Below 0.6", text_align='center'))
                                ],
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("Normal", text_align='center')),
                                    ft.DataCell(ft.Text("0.6 - 1.4", text_align='center'))
                                ],
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("High", text_align='center')),
                                    ft.DataCell(ft.Text("Above 1.4", text_align='center'))
                                ],
                            ),
                        ],
                    ),
            )
            
            myresult.controls.append(
                    ft.Divider()
            )
            
            progress_bar.value = 1
            container.visible = False
            page.update()
                
                
    def handle_file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:
            container.visible = True
            progress_bar.value = 0.2
            page.update()
            
            ufile = e.files[0]
            
            img_in = f'{ufile.path}'
            pred, ib, sim, ssim = fetch_compute(img_in)
            # print(sim, ssim, pred)
            
            if 'Error' in pred:
                myresult.controls.clear()
                myresult.controls.append(
                    ft.Text(f'Server is not Reachable! Please try again Later!', size=20)
                )
                container.visible = False
                page.update()
                
            elif int(sim*100) < IMG_COLOR_COMPARE_THRESHOLD or int(ssim*100) < IMG_STRUCTURE_COMPARE_THRESHOLD:
                myresult.controls.clear()
                myresult.controls.append(
                    ft.Text(f'Invalid Image! Please try again!', size=20)
                )
                container.visible = False
                page.update()
                
            else:
                progress_bar.value = 0.8
                page.update()
                # Update the displayed image:
                with open(img_in, "rb") as image_file:
                    image_data = image_file.read()
                    base64_string = base64.b64encode(image_data).decode('utf-8')
                img_width = page.width * 0.5
                aspect_ratio = 16 / 10
                img_height = img_width / aspect_ratio
                time.sleep(0.2)
                
                myresult.controls.clear()
                myresult.controls.append(
                    ft.Row([
                        ft.Image(src_base64=base64_string, width=img_width, height=img_height, fit=ft.ImageFit.CONTAIN, border_radius=ft.border_radius.all(5)),
                        ft.Image(src_base64=ib, width=img_width, height=img_height, fit=ft.ImageFit.CONTAIN, border_radius=ft.border_radius.all(5))
                    ], alignment=ft.MainAxisAlignment.CENTER)
                )
                progress_bar.value = 0.9
                page.update()
                
                myresult.controls.append(ft.Divider())
                myresult.controls.append(
                    ft.Text(f'Creatinine Level: {pred.capitalize()}', size=20, height=60)
                )
                myresult.controls.append(
                    ft.Divider()
                )
                myresult.controls.append(
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Creatinine Level", text_align='center')),
                            ft.DataColumn(ft.Text("Creatinine Range (mg/dL)", text_align='center'))
                        ],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("Low", text_align='center')),
                                    ft.DataCell(ft.Text("Below 0.6", text_align='center'))
                                ],
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("Normal", text_align='center')),
                                    ft.DataCell(ft.Text("0.6 - 1.4", text_align='center'))
                                ],
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("High", text_align='center')),
                                    ft.DataCell(ft.Text("Above 1.4", text_align='center'))
                                ],
                            ),
                        ],
                    ),
                )
                
                myresult.controls.append(
                    ft.Divider()
                )
                
                progress_bar.value = 1
                container.visible = False
                page.update()
            

    def open_file_picker(e):
        file_picker.pick_files(allow_multiple=False, allowed_extensions=['jpg'])
        
        
    def changetheme(e):
        
        page.splash.visible = True
        page.theme_mode = "light" if page.theme_mode =="dark" else "dark"
        page.update()
 
        time.sleep(0.5)
        toggledarklight.selected = not toggledarklight.selected
        page.splash.visible = False
        page.update()
        

    page.theme_mode = 'dark'
    file_picker = ft.FilePicker(on_result=handle_file_picker_result)
    myresult = ft.Column(horizontal_alignment='center')
    
    toggledarklight = ft.IconButton(
        on_click=changetheme,
        icon='dark_mode',
        selected_icon='light_mode',
        style=ft.ButtonStyle(
            color={'': ft.colors.BLACK, 'selected': ft.colors.WHITE}
        )
    )

    page.appbar = ft.AppBar(
        toolbar_height=80,
        title=ft.Text('KCDetector', size=40, weight="bold"),
        center_title=False,
        bgcolor='blue',
        actions=[
            toggledarklight
        ]
    )
    
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.splash = ft.ProgressBar(visible=False)
    
    # Create a progress bar and a text area:
    progress_bar = ft.ProgressBar(width=page.width)
    status_text = ft.Text("Processing Image...", size=12)
    container = ft.Column(
        controls=[
            progress_bar,
            status_text,
        ],
        visible=False,
        alignment="center"
    )
    page.add(container)
    
    # Main layout
    page.add(
        ft.Column([
            ft.Text(' ', size=20),
            ft.Row([
                ft.Column([
                    ft.Text(
                        "Upload an Image", 
                        size=30
                    ),
                    ft.Row([
                        ft.ElevatedButton(
                            "Gallery",
                            bgcolor="green",
                            color="white",
                            on_click=open_file_picker
                        ),
                        ft.ElevatedButton(
                            "Demo",
                            bgcolor="white",
                            color="green",
                            on_click=run_demo
                        )
                    ])
                ],
                horizontal_alignment='center'),
                
                ft.Column([
                    ft.Image(src=f'/ref.jpg', width=100, height=100, fit=ft.ImageFit.CONTAIN),
                    ft.Text('<Reference Image>', size=10)
                ],
                horizontal_alignment='center')
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND),
            
            ft.Divider(),
            myresult        
        ],
        horizontal_alignment='center'),
    )

    page.overlay.append(file_picker)
    page.update()


app = ft.app(target=main, assets_dir='assets')