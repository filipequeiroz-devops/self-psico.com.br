# Migrating existing infrastructure created via the AWS console to Terraform.
# Migrando infraestrutura já criada via console da AWS para o Terraform

**Language / Idioma**: [🇺🇸 English](#-project-overview) | [🇧🇷 Português](#-visão-geral-do-projeto)

<div align="center">

![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon%20S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)
![Amazon API Gateway](https://img.shields.io/badge/Amazon%20API%20Gateway-FF4F8B?style=for-the-badge&logo=amazonapigateway&logoColor=white) 
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![CI/CD](https://github.com/filipequeiroz-devops/self-psico.com.br/actions/workflows/deploy.yaml/badge.svg)
</div>

---

## 🇺🇸 Project Overview

The goal of this project was to migrate an existing infrastructure to be managed by Terraform. I developed a website (a real-world project) and architected the entire environment using the AWS Console initially. Once everything was fully functional—including AWS Lambda, API Gateway, and S3 buckets—I migrated the resources into a `.tfstate` file to implement Infrastructure as Code (IaC).

### 🏗️ Steps I took

1.  **Terraform import:** I consulted the Terraform documentation for each AWS resource to use the correct `import` command for the existing infrastructure.
2.  **Terraform show:** After importing the resources, I needed to create the `.tf` files. I used the `terraform show` command to inspect the current resource configurations, allowing me to accurately map them into my Terraform code.
3.  **Test and Standardization:** During the migration, I noticed that some resource properties were imported as `null` when they should have had values. This was particularly evident with the API Gateway, where the `target` (Integration ID) came up as `null`. I manually adjusted the `.tf` files to match the actual AWS environment. Finally, I tested the website's functionality to ensure the migration was successful.
4.  **Implemented GitHub Actions:** Since the website is hosted in an S3 bucket, I set up a GitHub Action to automatically sync the website files to the bucket upon every `git push`. This ensures that any changes are immediately reflected in the live environment.

> **Live Demo:** [Check it working here](https://self-psico.com.br/)

---

## 🇧🇷 Visão Geral do Projeto

Este projeto consiste na migração de uma infraestrutura existente para ser gerenciada pelo Terraform. Eu desenvolvi um site (projeto real) e arquitetei todo o ambiente utilizando inicialmente o Console da AWS. Com tudo já funcionando — AWS Lambda, API Gateway e buckets S3 — realizei a migração de todos os recursos para o arquivo de estado `.tfstate`.

### 🏗️ Passos que realizei

1.  **Terraform import:** Li a documentação dos recursos da AWS no Terraform para verificar os comandos de importação de cada recurso da infraestrutura.
2.  **Terraform show:** Após importar os recursos, eu ainda precisava criar os arquivos `.tf`. Usei o comando `terraform show` para visualizar as configurações dos recursos e, assim, copiar e estruturar o código nos arquivos de configuração.
3.  **Teste e Padronização:** Mesmo após o `import` e o `show`, notei que algumas propriedades vieram como `null` quando deveriam conter valores. Isso aconteceu especialmente com o API Gateway, onde o campo `target` (que deveria mostrar o ID de integração) veio vazio. Este passo foi necessário para que meus arquivos `.tf` refletissem exatamente a infraestrutura existente na AWS. Após os ajustes, testei as funções do site e tudo funcionou perfeitamente.
4.  **Implementação de GitHub Actions:** Como o site está hospedado em um bucket S3, utilizei GitHub Actions para enviar automaticamente os arquivos do site para o bucket de origem sempre que houver modificações após um `git push`. Assim, as alterações são refletidas no site automaticamente.

---

### 🚀 Tech Stack & Testing

* **Cloud:** AWS (Lambda, API Gateway, DynamoDB, S3).
* **IaC:** Terraform.
* **CI/CD:** GitHub Actions para deploy automatizado.

---

<div align="center">
  <sub>Developed by **Filipe Queiroz** as part of a DevOps & SRE Career Transition Portfolio.</sub>
</div>