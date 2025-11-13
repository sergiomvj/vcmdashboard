// SCRIPT DE BIOGRAFIAS CORRIGIDO - USA DADOS REAIS DO SUPABASE
import { createClient } from '@supabase/supabase-js';
import fs from 'fs';
import path from 'path';

// Credenciais REAIS (mesma aplicação web)
const supabaseUrl = 'https://fzyokrvdyeczhfqlwxzb.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ6eW9rcnZkeWVjemhmcWx3eHpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI1MDQzMzAsImV4cCI6MjA3ODA4MDMzMH0.mf3TC1PxNd9pe9M9o-D_lgqZunUl0kPumS0tU4oKodY';

const supabase = createClient(supabaseUrl, supabaseKey);

console.log('🚀 SCRIPT BIOGRAFIA REAL - CONECTADO AO SUPABASE VCM');
console.log('===================================================');

async function generateRealBiografias() {
  try {
    // 1. BUSCA EMPRESA REAL COM PERSONAS
    console.log('1️⃣ Buscando empresas com personas...');
    
    const { data: empresas, error: empresasError } = await supabase
      .from('empresas')
      .select('*')
      .eq('status', 'ativa')
      .gt('total_personas', 0)  // Só empresas com personas
      .order('total_personas', { ascending: false });
    
    if (empresasError) {
      console.log('❌ Erro ao buscar empresas:', empresasError);
      return;
    }
    
    if (empresas.length === 0) {
      console.log('❌ Nenhuma empresa com personas encontrada!');
      return;
    }
    
    // Usar a empresa com mais personas (LifewayUSA)
    const empresaPrincipal = empresas[0];
    console.log(`✅ Empresa selecionada: ${empresaPrincipal.nome}`);
    console.log(`   Total personas: ${empresaPrincipal.total_personas}`);
    
    // 2. BUSCA PERSONAS REAIS DESTA EMPRESA
    console.log('\n2️⃣ Buscando personas reais...');
    
    const { data: personas, error: personasError } = await supabase
      .from('personas')
      .select('*')
      .eq('empresa_id', empresaPrincipal.id)
      .eq('status', 'active')
      .order('full_name', { ascending: true });
    
    if (personasError) {
      console.log('❌ Erro ao buscar personas:', personasError);
      return;
    }
    
    console.log(`✅ ${personas.length} personas encontradas!`);
    
    // 3. GERA BIOGRAFIA PARA PRIMEIRA PERSONA COMO TESTE
    if (personas.length > 0) {
      const personaTest = personas[0];
      console.log(`\n3️⃣ Gerando biografia para: ${personaTest.full_name}`);
      
      const biografia = await generateBiografiaForPersona(personaTest, empresaPrincipal);
      
      if (biografia) {
        // 4. SALVA BIOGRAFIA NO ARQUIVO
        await saveBiografiaToFile(personaTest, biografia);
        
        // 5. ATUALIZA STATUS NO BANCO
        await updateBiografiaStatus(empresaPrincipal.id, personaTest.id);
        
        console.log('✅ BIOGRAFIA GERADA COM SUCESSO!');
        console.log('\n🎯 RESULTADOS:');
        console.log(`   • Empresa: ${empresaPrincipal.nome} (REAL)`);
        console.log(`   • Persona: ${personaTest.full_name} (REAL)`);
        console.log(`   • Status biografia: ATIVO`);
        console.log(`   • Dados: CONECTADOS AO SUPABASE`);
      }
    }
    
  } catch (error) {
    console.log('💥 Erro geral:', error);
  }
}

async function generateBiografiaForPersona(persona, empresa) {
  // Biografia simples usando dados reais
  const biografia = `# ${persona.full_name}

## INFORMAÇÕES BÁSICAS
- **Nome Completo:** ${persona.full_name}
- **Cargo:** ${persona.role}
- **Departamento:** ${persona.department || 'N/A'}
- **Email:** ${persona.email || 'N/A'}
- **WhatsApp:** ${persona.whatsapp || 'N/A'}

## EMPRESA
- **Empresa:** ${empresa.nome}
- **Código:** ${empresa.codigo}
- **Setor:** ${empresa.industria}
- **País:** ${empresa.pais}

## EXPERIÊNCIA
- **Anos de experiência:** ${persona.experiencia_anos || 'N/A'} anos
- **Status:** ${persona.status}

## PERSONALIDADE
${JSON.stringify(persona.personalidade || {}, null, 2)}

## IA CONFIGURATION
- **Temperatura IA:** ${persona.temperatura_ia || 'N/A'}
- **Max Tokens:** ${persona.max_tokens || 'N/A'}

## BIOGRAFIA COMPLETA
${persona.biografia_completa || 'Biografia a ser desenvolvida com dados reais do Supabase.'}

---
*Biografia gerada com dados REAIS do Supabase VCM Central*  
*Data: ${new Date().toLocaleString('pt-BR')}*  
*Empresa: ${empresa.nome} (ID: ${empresa.id})*
`;

  return biografia;
}

async function saveBiografiaToFile(persona, biografia) {
  // Cria diretório se não existir
  const dir = path.join(process.cwd(), '04_BIOS_PERSONAS_REAL', sanitizeName(persona.full_name));
  
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  // Salva arquivo
  const filename = path.join(dir, `${sanitizeName(persona.full_name)}_bio.md`);
  fs.writeFileSync(filename, biografia, 'utf-8');
  
  console.log(`   💾 Biografia salva: ${filename}`);
}

function sanitizeName(name) {
  return name.replace(/[^a-zA-Z0-9\s]/g, '').replace(/\s+/g, '_');
}

async function updateBiografiaStatus(empresaId, personaId) {
  try {
    // Atualiza status da biografia na empresa
    const { data: empresa, error: empresaError } = await supabase
      .from('empresas')
      .select('scripts_status')
      .eq('id', empresaId)
      .single();
      
    if (!empresaError && empresa) {
      const newStatus = {
        ...empresa.scripts_status,
        biografias: true  // Marca biografia como concluída
      };
      
      await supabase
        .from('empresas')
        .update({ 
          scripts_status: newStatus,
          updated_at: new Date().toISOString()
        })
        .eq('id', empresaId);
        
      console.log('   ✅ Status biografia atualizado no banco!');
    }
    
  } catch (error) {
    console.log('   ⚠️ Erro ao atualizar status:', error.message);
  }
}

// Executa o script
console.log('🏁 Iniciando geração de biografias com dados REAIS...\n');
generateRealBiografias();