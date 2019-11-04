function plotRealVSPredicted(models, colors, suffix, day, building, xLimit, modelNames)
    x = 1:xLimit;
    nModels = size(models,2)
    maxYAxis = 0
    for i=1:nModels %models
        model = models{1,i}(1:xLimit,day);
        plot(x, model.', colors{1,i},'LineWidth',1,'MarkerSize',2);hold on;
        yAxisLimit = max(model)
        if yAxisLimit > maxYAxis
            maxYAxis = yAxisLimit
        end 
    end
    %plot(x, real, colors(1),'LineWidth',1.5,'MarkerSize',marker_size);hold on;

    ylabel('Consumption (hours)','FontSize', 10);
    xlabel(strcat('Day',{' '}, num2str(day),' prediction  for each test sample'),'FontSize', 10);
    %[0 50 100 150 200 250 300 350 400 450 500 550 600]
    %[0 100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800]
    xticks(0:50:xLimit);%0:xLimit:10
    yaxis = 0:100:maxYAxis;
    yticks(yaxis);
    ylim([10 maxYAxis]);
    
    legend(modelNames,'FontSize', 14);%,'FontName','Times New Roman'

    legend boxoff;
    set(gca,'box','off');
    set(gcf, 'Position', [500, 300, 1000, 500]); %800 refers to width, 340 to height
    set(gca,'fontsize', 18)  ;
    
    nameFile = strcat('../Images/',num2str(day),building,char(suffix)) %,auxBuild{1},'/' ,'predicted_v_real')
    saveas(gcf,nameFile,'epsc')
    clf
end