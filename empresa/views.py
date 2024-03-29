from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Tecnologias, Empresa, Vagas, Profissao
from django.contrib import messages
from django.contrib.messages import constants
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def nova_empresa(request):
    if request.method == "GET":
        techs = Tecnologias.objects.all()
        prof = Profissao.objects.all()        
        return render(request, 'nova_empresa.html', {'techs': techs, 'prof':prof})
    elif request.method == 'POST':
        
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        email = request.POST.get('email')
        logo = request.FILES.get('logo')

        cep = request.POST.get('cep')        
        logradouro = request.POST.get('logradouro')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')

        profissoes = request.POST.getlist('profissoes')
        tecnologias = request.POST.getlist('tecnologias')
        caracteristicas = request.POST.get('caracteristicas')

        
        if (len(nome.strip()) == 0 or len(email.strip()) == 0 or len(cep.strip()) == 0 or len(logradouro.strip()) == 0 or
            len(bairro.strip()) == 0 or len(numero.strip()) == 0 or len(cidade.strip()) == 0 or len(estado.strip()) == 0
            or len(caracteristicas.strip()) == 0 or (not logo)):
            messages.add_message(request, constants.ERROR,'Preencha todos os campos')
            return redirect('/home/nova_empresa')

        if logo.size > 100_000_000:
            messages.add_message(request, constants.WARNING,
                                 'A logo da empresa deve ter menos de 10MB')
            return redirect('/home/nova_empresa')

        

        empresa = Empresa(logo=logo,
                          nome=nome,
                          cnpj=cnpj,
                          email=email,
                          cep=cep,
                          logradouro=logradouro,
                          numero=numero,
                          bairro=bairro,
                          cidade=cidade,
                          estado=estado,                          
                          caracteristica_empresa=caracteristicas)

        empresa.save()
        empresa.tecnologias.add(*tecnologias)
        empresa.profissao_empresa.add(*profissoes)
        empresa.save()
        messages.add_message(request, constants.SUCCESS,
                             'Empresa cadastrada com sucesso')
        return redirect('/home/empresas')


def empresas(request):
    tecnologias_filtrar = request.GET.get('tecnologias')
    nome_filtrar = request.GET.get('nome')
    
    empresas = Empresa.objects.all()
    
    # 5 empresas por página
    paginator = Paginator(empresas, 3)
    # número da página atual
    pagina = request.GET.get('page')

    try:
        empresas = paginator.page(pagina)
    except PageNotAnInteger:
         empresas = paginator.page(1)
    except EmptyPage:
        empresas = paginator.page(paginator.num_pages)
        
    if tecnologias_filtrar:
        empresas = empresas.filter(tecnologias=tecnologias_filtrar)

    if nome_filtrar:
        empresas = empresas.filter(nome__icontains=nome_filtrar)

    tecnologias = Tecnologias.objects.all()
    return render(request, 'empresa.html', {'empresas': empresas, 'tecnologias': tecnologias})


def excluir_empresa(request, id):
    empresa = Empresa.objects.get(id=id)
    empresa.delete()
    messages.add_message(request, constants.SUCCESS,
                         'Empresa excluída com sucesso')
    return redirect('/home/empresas')


def empresa(request, id):
    empresa_unica = get_object_or_404(Empresa, id=id)
    empresas = Empresa.objects.all()
    tecnologias = Tecnologias.objects.all()
    profissao = Profissao.objects.all()
    vagas = Vagas.objects.filter(empresa_id=id)
    return render(request, 'empresa_unica.html', {'empresa': empresa_unica,
                                                  'tecnologias': tecnologias,
                                                  'profissao': profissao,
                                                  'empresas': empresas,
                                                  'vagas': vagas})

def editar_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)


    if request.method == "GET":
        techs = Tecnologias.objects.all()        
        prof = Profissao.objects.all()               
        return render(request, 'editar_empresa.html', {'empresa': empresa, 'techs': techs, 'prof': prof})
    
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        email = request.POST.get('email')
        logo = request.FILES.get('logo')

        cep = request.POST.get('cep')        
        logradouro = request.POST.get('logradouro')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')

        profissoes = request.POST.getlist('profissoes')
        tecnologias = request.POST.getlist('tecnologias')
        caracteristicas = request.POST.get('caracteristicas')
        
        if not all([nome, cnpj, email, cep, logradouro, bairro, numero, cidade, estado, profissoes, tecnologias, caracteristicas]) or not all([campo.strip() for campo in [nome, cnpj, email, cep, logradouro, bairro, numero, cidade, estado, caracteristicas] if campo]) or not all([campo.strip() for campo in profissoes if campo]) or not all([campo.strip() for campo in tecnologias if campo]):
            messages.add_message(request, constants.ERROR,'Preencha todos os campos')
            return redirect(f'/home/editar_empresa/{id}')


        if logo:
            if logo.size > 100_000_000:
                messages.add_message(request, constants.WARNING,
                                     'A logo da empresa deve ter menos de 10MB')
                return redirect(f'/home/editar_empresa/{id}')

        
        empresa.logo = logo if logo else empresa.logo
        empresa.nome = nome
        empresa.cnpj = cnpj
        empresa.email = email
        empresa.cep = cep
        empresa.logradouro = logradouro
        empresa.numero = numero
        empresa.bairro = bairro
        empresa.cidade = cidade
        empresa.estado = estado        
        empresa.caracteristica_empresa = caracteristicas
       
        
        empresa.save()
        empresa.tecnologias.set(tecnologias)
        empresa.profissao_empresa.set(profissoes)
        messages.add_message(request, constants.SUCCESS,
                             'Empresa atualizada com sucesso')
        return redirect(f'/home/empresas/')
