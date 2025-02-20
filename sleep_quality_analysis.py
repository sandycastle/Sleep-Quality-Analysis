
import pandas as pd
import numpy as np

DATA_FILE = 'saude_do_sono_estilo_vida.csv'
translation_dict = {
    'ID': 'ID',
    'Gênero': 'Gender',
    'Idade': 'Age',
    'Ocupação': 'Occupation',
    'Duração do sono': 'Sleep Duration',
    'Qualidade do sono': 'Sleep Quality',
    'Nível de atividade física': 'Physical Activity Level',
    'Nível de estresse': 'Stress Level',
    'Categoria BMI': 'BMI Category',
    'Pressão sanguíneaaaa': 'Blood Pressure',
    'Frequência cardíaca': 'Heart Rate',
    'Passos diários': 'Daily Steps',
    'Distúrbio do sono': 'Sleep Disorder',
    'Homem': 'Male',
    'Mulher': 'Female',
    'Eng. de Software': 'Software Engineer',
    'Médico(a)': 'Doctor',
    'Representante de Vendas': 'Sales Representative',
    'Professor(a)': 'Teacher',
    'Enfermeiro(a)': 'Nurse',
    'Engenheiro(a)': 'Engineer',
    'Contador(a)': 'Accountant',
    'Cientista': 'Scientist',
    'Advogado(a)': 'Lawyer',
    'Pessoa Vendendora': 'Salesperson',
    'Nenhuma': 'None',
    'Apneia do sono': 'Sleep Apnea',
    'Insônia': 'Insomnia',
    'Sobrepeso': 'Overweight',
    'Peso normal': 'Normal weight',
    'Obesidade': 'Obesity',
    'Gerente': 'Manager'
}

def main():
    # Read the CSV file
    df_sleep = pd.read_csv(DATA_FILE)
    #translate from Portuguese to English
    translate(df_sleep)

    print("1. What is the average, mode and median hours of sound for each profession? ")
    print(calcs(df_sleep))

    print("2. What percentage of people working in software engineering are obese?")
    print(check_obesity(df_sleep, 'Software Engineer'))
   
    print("3. According to the data, do lawyers or sales representatives sleep less?")
    print(less_sleep(df_sleep, ['Lawyer', 'Sales Representative']))

    print("4. Between those who studied nursing and those who studied medicine, who has fewer hours of sleep?")
    print(less_sleep_comparative(df_sleep, 'Nurse', 'Doctor'))

    print("5. Create a subset with the columns ID, Gender, Age, Blood Pressure, and Heart Rate.")
    subset = df_sleep[['ID','Gender', 'Age', 'Blood Pressure', 'Heart Rate']]
    print(subset.head())

    print("6. What is the profession with the fewest people in the dataset?")
    print(least_frequent(df_sleep))

    print("7. Who has higher average blood pressure, men or women?")
    print(higher_avg_blood_pressure(df_sleep))

    print("8. Is it predominant among participants to sleep 8 hours per day (consider using Mode as a measure)?")
    print('Yes' if sleep_mode(df_sleep) == 8 else 'No')

    print("9. Do people with heart rates above 70 take more steps than people with heart rates less than or equal to 70?")
    print('Yes' if more_steps_per_heart_rate(df_sleep, 70) else 'No')


def translate(ds):
    # Translate column headers
    ds.rename(columns=translation_dict, inplace=True)
    # Translate content
    ds.replace(translation_dict, inplace=True)
    return ds

def calcs(ds):
    # Calculate average, mode and median hours of sleep for each profession
    avg = ds.groupby('Occupation')['Sleep Duration'].mean()
    mode = ds.groupby('Occupation')['Sleep Duration'].apply(lambda x: x.mode().iloc[0])
    median = ds.groupby('Occupation')['Sleep Duration'].median()

    # Combine the results
    result = pd.concat([avg, mode, median], axis=1)
    result.columns = ['Average', 'Mode', 'Median']

    return result

def check_obesity(ds, occupation):
    sofeng = ds[ds['Occupation'] == occupation]
    sofeng_bmi = sofeng['BMI Category'].value_counts(normalize=True) * 100
    return f"{sofeng_bmi['Obesity']}%"

def less_sleep(ds, ocuppation):
    general_avg = ds['Sleep Duration'].mean()
    ocup_avg = ds[ds['Occupation'].isin(ocuppation)]['Sleep Duration'].mean()
    return ocup_avg < general_avg

def less_sleep_comparative(ds, occupation1, occupation2):
    occp1 = ds[ds['Occupation'] == occupation1]
    occp2 = ds[ds['Occupation'] == occupation2]
    occp1_sleep = occp1['Sleep Duration'].mean()
    occp2_sleep = occp2['Sleep Duration'].mean()
    
    if occp1_sleep < occp2_sleep:
        return occupation1
    else:    
        return occupation2
    
def least_frequent(ds):
    return ds['Occupation'].value_counts().idxmin()

def higher_avg_blood_pressure(ds):
    ds[['Systolic', 'Diastolic']] = ds['Blood Pressure'].apply(lambda x: pd.Series(parse_bp(x)))

    avg_systolic_men = ds[ds['Gender'] == 'Male']['Systolic'].mean()
    avg_diastolic_men = ds[ds['Gender'] == 'Male']['Diastolic'].mean()
    avg_systolic_women = ds[ds['Gender'] == 'Female']['Systolic'].mean()
    avg_diastolic_women = ds[ds['Gender'] == 'Female']['Diastolic'].mean()

    avg_bp_men = (avg_systolic_men + avg_diastolic_men) / 2
    avg_bp_women = (avg_systolic_women + avg_diastolic_women) / 2
    if avg_bp_men > avg_bp_women:
        return 'Men'
    else:
        return 'Women'
    
def parse_bp(bp):
    systolic, diastolic = map(int, bp.split('/'))
    return systolic, diastolic

def sleep_mode(ds):
    return ds['Sleep Duration'].mode()[0]

def more_steps_per_heart_rate(ds, rate):
    avg_hr_above = ds[ds['Heart Rate'] > rate]['Daily Steps'].mean()
    avg_hr_below = ds[ds['Heart Rate'] <= rate]['Daily Steps'].mean()
    return avg_hr_above > avg_hr_below

main()

