# liderTCP

Work implemented in Python using threads to elect a leader among several connected machines, each sends a heartbeat every period of time and a new leader is chosen whenever the current leader is disconnected. The leader is chosen based on the lowest ID.

System requirements

Firstly, it is necessary to create the 'entry' file in the same directory as the code and containing the necessary information so that the system can make the necessary connections. As the file is read line by line, the information must be in the following structure:

1st line, contains the number of peers.

2nd line onwards contains the ID followed by the IP of the machines, always one machine per line

Example: 

> 4
> 0 192.168.0.6
> 1 192.168.0.7
> 2 192.168.0.8
> 3 192.168.0.9

*É importante lembrar que a relação dos IDs com os IPs deve ser respeitado durante todo o processo e deve ser utilizado o mesmo arquivo 'entrada' para todas as máquinas.

# Inicialização do sistema

Feito isso podemos executar o programa, para isso, basta executar o programa python com os primeiro argumento sendo o seu próprio ID e o segundo argumento a porta que será feita a conexão. Exemplo: python peer.py 0 5621
Então, o programa pega as informações retiradas do arquivo 'entrada' e armazenado em uma lista chamado IPs, esta lista oferece as informações que serão utilizadas para enviar mensagens e identificar os IPs das máquinas baseado nos IDs, até mesmo o seu próprio ID é obtido desta forma. Durante a leitura, o dicionário heartbeats, que tem como chave os IDs, é iniciado com zero e adicionamos os IDs na lista de máquinas onlines. É criado também uma thread para que o peer fique escutando se tem mensagens chegando junto com uma thread para verificar TIMEOUTS, mas só terá início quando todos estiverem conectados. Aqui ele permanece esperando até que todas as outras máquinas se conectem.

Até aqui, algumas decisões importante foram tomadas, uma delas é que o dicionário heartbeats irá armazenar o tempo que ele recebeu a mensagem, já pensando em posteriormente utilizar o TIMEOUT para encontrar as máquinas que desconectaram. Junto com isso, a forma para saber que todas as máquinas estão conectadas, é verificando que todos os heartbeats estão diferentes de 0 (zero). Também foi criado uma lista com as máquinas que é inicialmente preenchido com todos os IDs no arquivo 'entrada', talvez seja um pouco precipitado colocar todas as máquinas como online antes delas estarem realmente conectadas, mas como é necessário que todas as máquinas estejam conectadas para começar todo o processo de eleger o líder e realmente funcionar, não afeta o funcionamento de modo algum.
Já as mensagens, decidimos que seria simplesmente o seu próprio ID, pois é fácil de tratar e podemos facilmente encontrar o seu IP pela lista IPs, tivemos essa inspiração do heartbeats, pois é sugestivo entender que é apenas uma mensagem para saber que está vivo e naturalmente saber quem está vivo.

# Execução do sistema

O envio das mensagens é baseado nos IDs que estão na lista de máquinas onlines e definimos como frequência 2s. Após todas as máquinas se conectarem, o dicionário de heartbeats é completado com o tempo que recebeu as mensagens e é feita a primeira eleição. O resultado da eleição é o menor ID na lista de máquinas onlines. A lista de máquinas onlines é alterada quando o TIMEOUT verificar que o tempo desde que uma determinada máquina mandou mensagem para ele ultrapassou um tempo que definimos como 5s, consequentemente, o ID daquela máquina é retirado da lista e se o ID foi do líder, é feito uma nova eleição. Nesse momento entra em ação as mensagens urgentes, que usamos a flag MSG_OOB, elas avisam para outras que é necessário uma atualização de líder.

# O fluxo é basicamente o seguinte:

1. O peer manda seu ID para todas as máquinas da lista de máquinas onlines

2. Quando o heartbeat é recebido, registramos seu tempo de chegada no dicionário heartbeats referente ao ID do remetente.

3. Em paralelo, a cada 2s os peers mandam seu heartbeat.

4. Também em paralelo, o TIMEOUT chega sempre se o tempo desde a última conexão ultrapassou 5s. Se sim, verifica se é o líder, caso tenha perdido a conexão com o líder mandamos uma mensagem urgente e elegemos um novo líder, se não for o líder, apenas tiramos da lista de máquinas online.
