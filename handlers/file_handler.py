import os
import pandas as pd
from tkinter import filedialog
import PyPDF2
from handlers.preprocess_module import preprocess_dataframe



SUPPORTED_FORMATS = ['.csv', '.xlsx', '.xls', '.txt', '.pdf']

def is_supported_file(file_path):
    return os.path.splitext(file_path)[1].lower() in SUPPORTED_FORMATS

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path and is_supported_file(file_path):
        return file_path
    return None

def browse_folder():
    folder_path = filedialog.askdirectory()
    return folder_path if folder_path else None

def read_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    try:
        if ext == '.csv':
            df = pd.read_csv(file_path)
        elif ext in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path)
        elif ext == '.txt':
            df = pd.read_csv(file_path, sep="\t", engine="python")
        elif ext == '.pdf':
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() + '\n'
            lines = text.split('\n')
            rows = [line.strip().split() for line in lines if line.strip()]
            max_len = max((len(row) for row in rows), default=0)
            df = pd.DataFrame(rows, columns=[f'Col{i+1}' for i in range(max_len)])
        else:
            print("Unsupported file format.")
            return None

        # 🔽 Add this line to apply preprocessing
        return preprocess_dataframe(df)

    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    

def get_file_list_from_folder(folder_path):
    return [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if is_supported_file(os.path.join(folder_path, f))
    ]
